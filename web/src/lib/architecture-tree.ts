import { safeId, safeLabel } from './mermaid-client';

export interface ArchComponentInput {
    name?: string;
    type?: string;
    file?: string;
    ecosystem?: string;
    dependencies?: string[];
}

export interface ArchFileSummary {
    file: string;
    count: number;
    samples: string[];
}

export interface ArchDepEdge {
    fromId: string;
    toId: string;
    weight: number;
}

export interface ArchTreeNode {
    id: string;
    parentId: string | null;
    path: string;
    label: string;
    totalComponents: number;
    directComponents: number;
    totalFiles: number;
    children: string[];
    topFiles: ArchFileSummary[];
    internalDeps: ArchDepEdge[];
}

export interface ArchTreePayload {
    repoLabel: string;
    hasTree: boolean;
    rootId: string;
    nodes: Record<string, ArchTreeNode>;
}

interface RawNode {
    id: string;
    segment: string;
    path: string;
    children: Map<string, RawNode>;
    files: Map<string, string[]>;
    fileCounts: Map<string, number>;
    totalComponents: number;
    directComponents: number;
    componentKeys: Set<string>;
}

const MAX_SVG_CHILD_BRANCHES = 4;
const MAX_SVG_FILE_NODES = 4;

function normalizePath(rawFile: string | undefined): { dirs: string[]; fileBase: string } {
    const normalized = String(rawFile || '')
        .trim()
        .replace(/\\/g, '/')
        .replace(/^\/+/, '')
        .replace(/^\.\//, '');
    if (!normalized) {
        return { dirs: [], fileBase: '(unknown)' };
    }
    const parts = normalized.split('/').filter(Boolean);
    if (parts.length <= 1) {
        return { dirs: [], fileBase: parts[0] || '(unknown)' };
    }
    return {
        dirs: parts.slice(0, -1),
        fileBase: parts[parts.length - 1] || '(unknown)',
    };
}

function createRawNode(id: string, segment: string, pathStr: string): RawNode {
    return {
        id,
        segment,
        path: pathStr,
        children: new Map(),
        files: new Map(),
        fileCounts: new Map(),
        totalComponents: 0,
        directComponents: 0,
        componentKeys: new Set(),
    };
}

/** Collapse single-child folder chains (except root) to eliminate redundant click depth. */
function compressSingleChildFolders(node: RawNode, isRoot: boolean): void {
    for (const child of node.children.values()) {
        compressSingleChildFolders(child, false);
    }
    if (isRoot) return;

    while (node.files.size === 0 && node.children.size === 1) {
        const onlyChild = node.children.values().next().value as RawNode | undefined;
        if (!onlyChild) break;
        node.segment = `${node.segment}/${onlyChild.segment}`;
        node.path = onlyChild.path;
        node.children = onlyChild.children;
        node.files = onlyChild.files;
        node.fileCounts = onlyChild.fileCounts;
        node.directComponents = onlyChild.directComponents;
    }
}

function recomputeCounts(node: RawNode): number {
    let total = node.directComponents;
    for (const child of node.children.values()) {
        total += recomputeCounts(child);
    }
    node.totalComponents = total;
    return total;
}

/** Build a compact, navigable directory-tree index from analysis architecture components. */
export function buildArchTreeIndex(
    repoLabel: string,
    components: ArchComponentInput[]
): ArchTreePayload {
    const root = createRawNode('root', repoLabel, '');
    if (!Array.isArray(components) || components.length === 0) {
        return {
            repoLabel,
            hasTree: false,
            rootId: 'root',
            nodes: {
                root: {
                    id: 'root',
                    parentId: null,
                    path: '',
                    label: repoLabel,
                    totalComponents: 0,
                    directComponents: 0,
                    totalFiles: 0,
                    children: [],
                    topFiles: [],
                    internalDeps: [],
                },
            },
        };
    }

    let nextId = 1;
    const rawCompLocations = new Map<string, string>();
    const rawDepsByDir = new Map<string, string[]>();

    for (const comp of components) {
        const name = String(comp?.name || '').trim();
        const type = String(comp?.type || 'COMPONENT').trim();
        const { dirs, fileBase } = normalizePath(comp?.file);

        let cur = root;
        for (const seg of dirs) {
            let next = cur.children.get(seg);
            if (!next) {
                const subPath = cur.path ? `${cur.path}/${seg}` : seg;
                next = createRawNode(`node_${nextId++}`, seg, subPath);
                cur.children.set(seg, next);
            }
            cur = next;
        }

        const dedupKey = `${fileBase}::${name || 'Component'}::${type}`;
        if (!cur.componentKeys.has(dedupKey)) {
            cur.componentKeys.add(dedupKey);
            cur.directComponents += 1;
            cur.fileCounts.set(fileBase, (cur.fileCounts.get(fileBase) || 0) + 1);
            if (!cur.files.has(fileBase)) {
                cur.files.set(fileBase, []);
            }
            const names = cur.files.get(fileBase)!;
            if (name && names.length < 4 && !names.includes(name)) {
                names.push(name);
            }
        }

        if (name && !rawCompLocations.has(name)) {
            rawCompLocations.set(name, cur.path);
        }
        const deps = Array.isArray(comp?.dependencies) ? comp.dependencies : [];
        if (deps.length > 0) {
            if (!rawDepsByDir.has(cur.path)) rawDepsByDir.set(cur.path, []);
            const arr = rawDepsByDir.get(cur.path)!;
            for (const dep of deps) {
                const depStr = String(dep || '').trim();
                if (depStr) arr.push(depStr);
            }
        }
    }

    compressSingleChildFolders(root, true);
    recomputeCounts(root);

    const nodes: Record<string, ArchTreeNode> = {};
    const pathToNodeId = new Map<string, string>();

    function collectPaths(node: RawNode, assignedId: string): void {
        pathToNodeId.set(node.path, assignedId);
        // Preserve descendant directory prefixes inside compressed paths
        for (const child of node.children.values()) {
            collectPaths(child, child.id);
        }
    }
    collectPaths(root, 'root');

    function resolveBucketForPath(targetDirPath: string, childPaths: Set<string>): string | null {
        if (!targetDirPath) return null;
        for (const cp of childPaths) {
            if (targetDirPath === cp || targetDirPath.startsWith(`${cp}/`)) {
                return pathToNodeId.get(cp) || null;
            }
        }
        return null;
    }

    function finalize(node: RawNode, parentId: string | null): void {
        const sortedChildren = Array.from(node.children.values()).sort(
            (a, b) => b.totalComponents - a.totalComponents || a.segment.localeCompare(b.segment)
        );
        const childPaths = new Set(sortedChildren.map((c) => c.path));

        const topFiles: ArchFileSummary[] = Array.from(node.files.entries())
            .map(([file, samples]) => ({
                file,
                count: node.fileCounts.get(file) || samples.length,
                samples,
            }))
            .sort((a, b) => b.count - a.count || a.file.localeCompare(b.file))
            .slice(0, 12);

        // Roll up cross-folder dependencies between this node's immediate children
        const depCounts = new Map<string, number>();
        for (const [srcDir, depNames] of rawDepsByDir.entries()) {
            const fromBucket = resolveBucketForPath(srcDir, childPaths);
            if (!fromBucket) continue;
            for (const depName of depNames) {
                const targetDir = rawCompLocations.get(depName);
                if (!targetDir) continue;
                const toBucket = resolveBucketForPath(targetDir, childPaths);
                if (toBucket && toBucket !== fromBucket) {
                    const edgeKey = `${fromBucket}::${toBucket}`;
                    depCounts.set(edgeKey, (depCounts.get(edgeKey) || 0) + 1);
                }
            }
        }

        const internalDeps: ArchDepEdge[] = Array.from(depCounts.entries())
            .map(([key, weight]) => {
                const [fromId, toId] = key.split('::');
                return { fromId, toId, weight };
            })
            .sort((a, b) => b.weight - a.weight)
            .slice(0, 10);

        nodes[node.id] = {
            id: node.id,
            parentId,
            path: node.path,
            label: node.segment,
            totalComponents: node.totalComponents,
            directComponents: node.directComponents,
            totalFiles: node.files.size,
            children: sortedChildren.map((c) => c.id),
            topFiles,
            internalDeps,
        };

        for (const child of sortedChildren) {
            finalize(child, node.id);
        }
    }

    finalize(root, null);

    return {
        repoLabel,
        hasTree: Object.keys(nodes).length > 1 || root.totalFiles > 0,
        rootId: 'root',
        nodes,
    };
}

/** Return ancestor breadcrumb chain from root down to `nodeId`. */
export function buildBreadcrumbs(
    payload: ArchTreePayload,
    nodeId: string
): Array<{ id: string; label: string }> {
    const chain: Array<{ id: string; label: string }> = [];
    let cur: ArchTreeNode | undefined = payload.nodes[nodeId] || payload.nodes[payload.rootId];
    const seen = new Set<string>();
    while (cur && !seen.has(cur.id)) {
        seen.add(cur.id);
        chain.push({ id: cur.id, label: cur.label });
        cur = cur.parentId ? payload.nodes[cur.parentId] : undefined;
    }
    return chain.reverse();
}

/** Generate a bounded, strictly top-down (`flowchart TD`) Mermaid DAG for a tree node. */
export function buildArchTreeGraph(payload: ArchTreePayload, activeNodeId: string): string {
    const current = payload.nodes[activeNodeId] || payload.nodes[payload.rootId];
    if (!current || !payload.hasTree) {
        return 'flowchart TD\n  empty["No Architectural Components Detected"]';
    }

    const lines: string[] = ['flowchart TD'];
    const focusLabel =
        current.id === payload.rootId
            ? `${current.label} (${current.totalComponents} components)`
            : `${current.path || current.label} (${current.totalComponents} components)`;
    lines.push(`  curr(["${safeLabel(focusLabel)}"])`);

    const childIds = current.children;
    const visibleChildIds = childIds.slice(0, MAX_SVG_CHILD_BRANCHES);
    const renderedNodeMap = new Map<string, string>();

    visibleChildIds.forEach((cid) => {
        const child = payload.nodes[cid];
        if (!child) return;
        const mermaidId = `child_${safeId(child.id)}`;
        renderedNodeMap.set(child.id, mermaidId);
        const subSuffix =
            child.children.length > 0
                ? `${child.totalComponents} comps · ${child.children.length} dirs`
                : `${child.totalComponents} comps · ${child.totalFiles} files`;
        lines.push(`  ${mermaidId}["${safeLabel(child.label)} (${subSuffix})"]`);
        lines.push(`  curr --> ${mermaidId}`);
    });

    if (childIds.length > visibleChildIds.length) {
        const hiddenCount = childIds.length - visibleChildIds.length;
        lines.push(`  more_dirs["+${hiddenCount} more modules (use selector above)"]`);
        lines.push(`  curr --> more_dirs`);
    }

    // When a node has only 1 child folder and no direct files (e.g. root -> src/specify_cli),
    // automatically expand its top grandchildren so the overview immediately reveals modules.
    if (visibleChildIds.length === 1 && current.topFiles.length === 0) {
        const onlyChild = payload.nodes[visibleChildIds[0]];
        const onlyChildMermaidId = renderedNodeMap.get(onlyChild?.id || '');
        if (onlyChild && onlyChildMermaidId && onlyChild.children.length > 0) {
            const grandSlice = onlyChild.children.slice(0, MAX_SVG_CHILD_BRANCHES);
            grandSlice.forEach((gid) => {
                const grand = payload.nodes[gid];
                if (!grand) return;
                const grandMermaidId = `child_${safeId(grand.id)}`;
                renderedNodeMap.set(grand.id, grandMermaidId);
                lines.push(
                    `  ${grandMermaidId}["${safeLabel(grand.label)} (${grand.totalComponents})"]`
                );
                lines.push(`  ${onlyChildMermaidId} --> ${grandMermaidId}`);
            });
            if (onlyChild.children.length > grandSlice.length) {
                lines.push(
                    `  more_grand["+${onlyChild.children.length - grandSlice.length} more in ${safeLabel(onlyChild.label)}"]`
                );
                lines.push(`  ${onlyChildMermaidId} --> more_grand`);
            }
        }
    }

    // Add direct files inside the current directory cleanly without widening subfolder rows
    if (visibleChildIds.length > 0 && current.topFiles.length > 0) {
        const sampleFile = current.topFiles[0]?.file || 'files';
        lines.push(
            `  direct_files("${current.totalFiles} direct file(s), e.g. ${safeLabel(sampleFile)}")`
        );
        lines.push(`  curr --> direct_files`);
    } else {
        const filesSlice = current.topFiles.slice(0, MAX_SVG_FILE_NODES);
        filesSlice.forEach((f, idx) => {
            const fid = `file_${idx}`;
            const sampleText = f.samples.length > 0 ? `: ${f.samples.slice(0, 2).join(', ')}` : '';
            lines.push(`  ${fid}("${safeLabel(f.file)}${safeLabel(sampleText)}")`);
            lines.push(`  curr --> ${fid}`);
        });
        if (current.totalFiles > filesSlice.length) {
            lines.push(`  more_files("+${current.totalFiles - filesSlice.length} more files")`);
            lines.push(`  curr --> more_files`);
        }
    }

    // Include rolled-up cross-folder dependencies among rendered children
    for (const dep of current.internalDeps) {
        const fromMid = renderedNodeMap.get(dep.fromId);
        const toMid = renderedNodeMap.get(dep.toId);
        if (fromMid && toMid) {
            lines.push(`  ${fromMid} -. "${dep.weight} refs" .-> ${toMid}`);
        }
    }

    return lines.join('\n');
}
