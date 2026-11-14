---
title: Architecture — remix-run/react-router
description: Arc42 and Pipeline report for remix-run/react-router
---

# Repository Architecture Analysis: remix-run/react-router

## Metadata
- **SHA**: `b830e2e7ac73b7d153ceedb27f12163b11ca7eda`
- **Primary Ecosystem**: JavaScript/TypeScript

## Quality Metrics
- **avg_cyclomatic_complexity**: 5.76
- **component_count**: 606
- **files_analyzed**: 1726
- **framework**: React (Vite)
- **loc**: 519573
- **max_cyclomatic_complexity**: 847
- **sloc**: 439974

# Architecture: remix-run/react-router

## Context
- **Repository**: `remix-run/react-router`
- **SHA**: `b830e2e7ac73b7d153ceedb27f12163b11ca7eda`
- **Ecosystem**: JavaScript/TypeScript
- **Framework**: Unknown

## Building Block View

```mermaid
graph TD;
    repo_root(["remix-run/react-router (606 components)"])
    dir_0_integration["integration (364)"]
    repo_root --> dir_0_integration
    sub_0_0__module_root_["(module root) (313)"]
    dir_0_integration --> sub_0_0__module_root_
    sub_0_1_rsc["rsc (31)"]
    dir_0_integration --> sub_0_1_rsc
    sub_0_2_helpers["helpers (20)"]
    dir_0_integration --> sub_0_2_helpers
    dir_1_playground["playground (119)"]
    repo_root --> dir_1_playground
    sub_1_0_rsc_vite_framework["rsc-vite-framework (23)"]
    dir_1_playground --> sub_1_0_rsc_vite_framework
    sub_1_1_rsc_vite["rsc-vite (21)"]
    dir_1_playground --> sub_1_1_rsc_vite
    sub_1_2_rsc_vite_7_framework["rsc-vite-7-framework (21)"]
    dir_1_playground --> sub_1_2_rsc_vite_7_framework
    sub_1_more["+10 more submodules (54)"]
    dir_1_playground --> sub_1_more
    dir_2_packages["packages (116)"]
    repo_root --> dir_2_packages
    sub_2_0_react_router["react-router (82)"]
    dir_2_packages --> sub_2_0_react_router
    sub_2_1_react_router_dev["react-router-dev (19)"]
    dir_2_packages --> sub_2_1_react_router_dev
    sub_2_2_create_react_router["create-react-router (8)"]
    dir_2_packages --> sub_2_2_create_react_router
    sub_2_more["+7 more submodules (7)"]
    dir_2_packages --> sub_2_more
    dir_3_tutorials["tutorials (4)"]
    repo_root --> dir_3_tutorials
    dir_4_scripts["scripts (2)"]
    repo_root --> dir_4_scripts
    dir_other_modules["+1 more modules (1)"]
    repo_root --> dir_other_modules
    sub_0_0__module_root_ -.->|"366 deps"| sub_2_0_react_router
    sub_2_0_react_router -.->|"188 deps"| sub_0_0__module_root_
    sub_0_0__module_root_ -.->|"127 deps"| sub_1_1_rsc_vite
    sub_0_0__module_root_ -.->|"112 deps"| sub_1_0_rsc_vite_framework
    sub_0_1_rsc -.->|"85 deps"| sub_1_1_rsc_vite
    sub_2_0_react_router -.->|"69 deps"| sub_2_2_create_react_router
    sub_0_1_rsc -.->|"60 deps"| sub_0_0__module_root_
    sub_0_1_rsc -.->|"36 deps"| sub_2_0_react_router
    sub_0_0__module_root_ -.->|"34 deps"| sub_0_1_rsc
    sub_1_0_rsc_vite_framework -.->|"32 deps"| sub_0_0__module_root_
    sub_1_1_rsc_vite -.->|"23 deps"| sub_0_0__module_root_
    sub_0_0__module_root_ -.->|"21 deps"| sub_2_1_react_router_dev
```

## Component Details

Showing top 60 representative components out of 606 across 6 module group(s):

- **Module `integration`** (364 components — UI_COMPONENT: 354, MODULE: 6, API_ROUTE: 4)
- **Module `playground`** (119 components — UI_COMPONENT: 103, MODULE: 13, API_ROUTE: 3)
- **Module `packages`** (116 components — UI_COMPONENT: 102, MODULE: 14)
- **Module `tutorials`** (4 components — UI_COMPONENT: 3, MODULE: 1)
- **Module `scripts`** (2 components — MODULE: 1, UI_COMPONENT: 1)
- **Module `(root)`** (1 components — MODULE: 1)

- **RSCStaticRouter** (`packages/react-router/lib/rsc/server.ssr.tsx`): UI_COMPONENT (deps: Await, AwaitContext, AwaitContextProvider, Book, BoundaryShell, CLIENT_NON_COMPONENT_EXPORTS (+53 more))
- **RSCHydratedRouter** (`packages/react-router/lib/rsc/browser.tsx`): UI_COMPONENT (deps: Await, AwaitContext, AwaitContextProvider, Book, BoundaryShell, CLIENT_NON_COMPONENT_EXPORTS (+50 more))
- **BrowserRouter** (`packages/react-router/lib/dom/lib.tsx`): UI_COMPONENT (deps: Await, AwaitContext, AwaitContextProvider, Book, CRITICAL_CSS_DATA_ATTRIBUTE, Dashboard (+44 more))
- **Form** (`packages/react-router/lib/dom/lib.tsx`): UI_COMPONENT (deps: Await, AwaitContext, AwaitContextProvider, Book, CRITICAL_CSS_DATA_ATTRIBUTE, Dashboard (+44 more))
- **Gallery** (`packages/react-router/lib/dom/lib.tsx`): UI_COMPONENT (deps: Await, AwaitContext, AwaitContextProvider, Book, CRITICAL_CSS_DATA_ATTRIBUTE, Dashboard (+44 more))
- **HashRouter** (`packages/react-router/lib/dom/lib.tsx`): UI_COMPONENT (deps: Await, AwaitContext, AwaitContextProvider, Book, CRITICAL_CSS_DATA_ATTRIBUTE, Dashboard (+44 more))
- **HistoryRouter** (`packages/react-router/lib/dom/lib.tsx`): UI_COMPONENT (deps: Await, AwaitContext, AwaitContextProvider, Book, CRITICAL_CSS_DATA_ATTRIBUTE, Dashboard (+44 more))
- **Link** (`packages/react-router/lib/dom/lib.tsx`): UI_COMPONENT (deps: Await, AwaitContext, AwaitContextProvider, Book, CRITICAL_CSS_DATA_ATTRIBUTE, Dashboard (+44 more))
- **NavLink** (`packages/react-router/lib/dom/lib.tsx`): UI_COMPONENT (deps: Await, AwaitContext, AwaitContextProvider, Book, CRITICAL_CSS_DATA_ATTRIBUTE, Dashboard (+44 more))
- **ScrollRestoration** (`packages/react-router/lib/dom/lib.tsx`): UI_COMPONENT (deps: Await, AwaitContext, AwaitContextProvider, Book, CRITICAL_CSS_DATA_ATTRIBUTE, Dashboard (+44 more))
- **SomeComponent** (`packages/react-router/lib/dom/lib.tsx`): UI_COMPONENT (deps: Await, AwaitContext, AwaitContextProvider, Book, CRITICAL_CSS_DATA_ATTRIBUTE, Dashboard (+44 more))
- **Root** (`packages/react-router/lib/dom/lib.tsx`): UI_COMPONENT (deps: Await, AwaitContext, AwaitContextProvider, Book, CRITICAL_CSS_DATA_ATTRIBUTE, Dashboard (+43 more))
- **Dashboard** (`packages/react-router/lib/hooks.tsx`): UI_COMPONENT (deps: Await, AwaitContext, AwaitContextProvider, Book, CRITICAL_CSS_DATA_ATTRIBUTE, DataRouterContext (+38 more))
- **DashboardMessages** (`packages/react-router/lib/hooks.tsx`): UI_COMPONENT (deps: Await, AwaitContext, AwaitContextProvider, Book, CRITICAL_CSS_DATA_ATTRIBUTE, DataRouterContext (+38 more))
- **File** (`packages/react-router/lib/hooks.tsx`): UI_COMPONENT (deps: Await, AwaitContext, AwaitContextProvider, Book, CRITICAL_CSS_DATA_ATTRIBUTE, DataRouterContext (+38 more))
- **ImportantForm** (`packages/react-router/lib/hooks.tsx`): UI_COMPONENT (deps: Await, AwaitContext, AwaitContextProvider, Book, CRITICAL_CSS_DATA_ATTRIBUTE, DataRouterContext (+38 more))
- **Invoices** (`packages/react-router/lib/hooks.tsx`): UI_COMPONENT (deps: Await, AwaitContext, AwaitContextProvider, Book, CRITICAL_CSS_DATA_ATTRIBUTE, DataRouterContext (+38 more))
- **Post** (`packages/react-router/lib/hooks.tsx`): UI_COMPONENT (deps: Await, AwaitContext, AwaitContextProvider, Book, CRITICAL_CSS_DATA_ATTRIBUTE, DataRouterContext (+38 more))
- **StaticRouter** (`packages/react-router/lib/dom/server.tsx`): UI_COMPONENT (deps: Await, AwaitContext, AwaitContextProvider, Book, CRITICAL_CSS_DATA_ATTRIBUTE, DataRouterContext (+38 more))
- **StaticRouterProvider** (`packages/react-router/lib/dom/server.tsx`): UI_COMPONENT (deps: Await, AwaitContext, AwaitContextProvider, Book, CRITICAL_CSS_DATA_ATTRIBUTE, DataRouterContext (+38 more))
- **ErrorBoundary** (`packages/react-router/lib/hooks.tsx`): UI_COMPONENT (deps: Await, AwaitContext, AwaitContextProvider, Book, CRITICAL_CSS_DATA_ATTRIBUTE, DataRouterContext (+37 more))
- **Await** (`packages/react-router/lib/components.tsx`): UI_COMPONENT (deps: AwaitContext, AwaitContextProvider, CRITICAL_CSS_DATA_ATTRIBUTE, Dashboard, DashboardMessages, DataRouterContext (+30 more))
- **Book** (`packages/react-router/lib/components.tsx`): UI_COMPONENT (deps: AwaitContext, AwaitContextProvider, CRITICAL_CSS_DATA_ATTRIBUTE, Dashboard, DashboardMessages, DataRouterContext (+30 more))
- **DataRoutes** (`packages/react-router/lib/components.tsx`): UI_COMPONENT (deps: AwaitContext, AwaitContextProvider, CRITICAL_CSS_DATA_ATTRIBUTE, Dashboard, DashboardMessages, DataRouterContext (+30 more))
- **MemoryRouter** (`packages/react-router/lib/components.tsx`): UI_COMPONENT (deps: AwaitContext, AwaitContextProvider, CRITICAL_CSS_DATA_ATTRIBUTE, Dashboard, DashboardMessages, DataRouterContext (+30 more))
- **Navigate** (`packages/react-router/lib/components.tsx`): UI_COMPONENT (deps: AwaitContext, AwaitContextProvider, CRITICAL_CSS_DATA_ATTRIBUTE, Dashboard, DashboardMessages, DataRouterContext (+30 more))
- **Outlet** (`packages/react-router/lib/components.tsx`): UI_COMPONENT (deps: AwaitContext, AwaitContextProvider, CRITICAL_CSS_DATA_ATTRIBUTE, Dashboard, DashboardMessages, DataRouterContext (+30 more))
- **Route** (`packages/react-router/lib/components.tsx`): UI_COMPONENT (deps: AwaitContext, AwaitContextProvider, CRITICAL_CSS_DATA_ATTRIBUTE, Dashboard, DashboardMessages, DataRouterContext (+30 more))
- **Router** (`packages/react-router/lib/components.tsx`): UI_COMPONENT (deps: AwaitContext, AwaitContextProvider, CRITICAL_CSS_DATA_ATTRIBUTE, Dashboard, DashboardMessages, DataRouterContext (+30 more))
- **RouterProvider** (`packages/react-router/lib/components.tsx`): UI_COMPONENT (deps: AwaitContext, AwaitContextProvider, CRITICAL_CSS_DATA_ATTRIBUTE, Dashboard, DashboardMessages, DataRouterContext (+30 more))
- **Routes** (`packages/react-router/lib/components.tsx`): UI_COMPONENT (deps: AwaitContext, AwaitContextProvider, CRITICAL_CSS_DATA_ATTRIBUTE, Dashboard, DashboardMessages, DataRouterContext (+30 more))
- **SomeParent** (`packages/react-router/lib/components.tsx`): UI_COMPONENT (deps: AwaitContext, AwaitContextProvider, CRITICAL_CSS_DATA_ATTRIBUTE, Dashboard, DashboardMessages, DataRouterContext (+30 more))
- **WithComponentProps** (`packages/react-router/lib/components.tsx`): UI_COMPONENT (deps: AwaitContext, AwaitContextProvider, CRITICAL_CSS_DATA_ATTRIBUTE, Dashboard, DashboardMessages, DataRouterContext (+30 more))
- **WithErrorBoundaryProps** (`packages/react-router/lib/components.tsx`): UI_COMPONENT (deps: AwaitContext, AwaitContextProvider, CRITICAL_CSS_DATA_ATTRIBUTE, Dashboard, DashboardMessages, DataRouterContext (+30 more))
- **WithHydrateFallbackProps** (`packages/react-router/lib/components.tsx`): UI_COMPONENT (deps: AwaitContext, AwaitContextProvider, CRITICAL_CSS_DATA_ATTRIBUTE, Dashboard, DashboardMessages, DataRouterContext (+30 more))
- **CRITICAL_CSS_DATA_ATTRIBUTE** (`packages/react-router/lib/dom/ssr/components.tsx`): UI_COMPONENT (deps: AwaitContext, AwaitContextProvider, Dashboard, DashboardMessages, DataRouterContext, DataRouterDataContext (+29 more))
- **FrameworkContext** (`packages/react-router/lib/dom/ssr/components.tsx`): UI_COMPONENT (deps: AwaitContext, AwaitContextProvider, Dashboard, DashboardMessages, DataRouterContext, DataRouterDataContext (+29 more))
- **Links** (`packages/react-router/lib/dom/ssr/components.tsx`): UI_COMPONENT (deps: AwaitContext, AwaitContextProvider, Dashboard, DashboardMessages, DataRouterContext, DataRouterDataContext (+29 more))
- **Meta** (`packages/react-router/lib/dom/ssr/components.tsx`): UI_COMPONENT (deps: AwaitContext, AwaitContextProvider, Dashboard, DashboardMessages, DataRouterContext, DataRouterDataContext (+29 more))
- **PrefetchPageLinks** (`packages/react-router/lib/dom/ssr/components.tsx`): UI_COMPONENT (deps: AwaitContext, AwaitContextProvider, Dashboard, DashboardMessages, DataRouterContext, DataRouterDataContext (+29 more))
- **Root** (`packages/react-router/lib/dom/ssr/components.tsx`): UI_COMPONENT (deps: AwaitContext, AwaitContextProvider, Dashboard, DashboardMessages, DataRouterContext, DataRouterDataContext (+29 more))
- **Scripts** (`packages/react-router/lib/dom/ssr/components.tsx`): UI_COMPONENT (deps: AwaitContext, AwaitContextProvider, Dashboard, DashboardMessages, DataRouterContext, DataRouterDataContext (+29 more))
- **Await** (`packages/react-router/lib/rsc/server.rsc.ts`): UI_COMPONENT (deps: Book, CRITICAL_CSS_DATA_ATTRIBUTE, DataRoutes, ENABLE_DEV_WARNINGS, ErrorBoundary, FrameworkContext (+28 more))
- **ServerRouter** (`packages/react-router/lib/dom/ssr/server.tsx`): UI_COMPONENT (deps: Await, Book, BoundaryShell, CRITICAL_CSS_DATA_ATTRIBUTE, DataRoutes, FrameworkContext (+26 more))
- **AwaitContext** (`packages/react-router/lib/context.ts`): UI_COMPONENT (deps: Await, Book, CRITICAL_CSS_DATA_ATTRIBUTE, DataRoutes, ENABLE_DEV_WARNINGS, ErrorBoundary (+23 more))
- **AwaitContextProvider** (`packages/react-router/lib/context.ts`): UI_COMPONENT (deps: Await, Book, CRITICAL_CSS_DATA_ATTRIBUTE, DataRoutes, ENABLE_DEV_WARNINGS, ErrorBoundary (+23 more))
- **DataRouterContext** (`packages/react-router/lib/context.ts`): UI_COMPONENT (deps: Await, Book, CRITICAL_CSS_DATA_ATTRIBUTE, DataRoutes, ENABLE_DEV_WARNINGS, ErrorBoundary (+23 more))
- **DataRouterDataContext** (`packages/react-router/lib/context.ts`): UI_COMPONENT (deps: Await, Book, CRITICAL_CSS_DATA_ATTRIBUTE, DataRoutes, ENABLE_DEV_WARNINGS, ErrorBoundary (+23 more))
- **DataRouterNavigationContext** (`packages/react-router/lib/context.ts`): UI_COMPONENT (deps: Await, Book, CRITICAL_CSS_DATA_ATTRIBUTE, DataRoutes, ENABLE_DEV_WARNINGS, ErrorBoundary (+23 more))
- **DataRouterStateContext** (`packages/react-router/lib/context.ts`): UI_COMPONENT (deps: Await, Book, CRITICAL_CSS_DATA_ATTRIBUTE, DataRoutes, ENABLE_DEV_WARNINGS, ErrorBoundary (+23 more))
- **FetchersContext** (`packages/react-router/lib/context.ts`): UI_COMPONENT (deps: Await, Book, CRITICAL_CSS_DATA_ATTRIBUTE, DataRoutes, ENABLE_DEV_WARNINGS, ErrorBoundary (+23 more))
- **IsDataRouteContext** (`packages/react-router/lib/context.ts`): UI_COMPONENT (deps: Await, Book, CRITICAL_CSS_DATA_ATTRIBUTE, DataRoutes, ENABLE_DEV_WARNINGS, ErrorBoundary (+23 more))
- **LocationContext** (`packages/react-router/lib/context.ts`): UI_COMPONENT (deps: Await, Book, CRITICAL_CSS_DATA_ATTRIBUTE, DataRoutes, ENABLE_DEV_WARNINGS, ErrorBoundary (+23 more))
- **NavigationContext** (`packages/react-router/lib/context.ts`): UI_COMPONENT (deps: Await, Book, CRITICAL_CSS_DATA_ATTRIBUTE, DataRoutes, ENABLE_DEV_WARNINGS, ErrorBoundary (+23 more))
- **RSCRouterContext** (`packages/react-router/lib/context.ts`): UI_COMPONENT (deps: Await, Book, CRITICAL_CSS_DATA_ATTRIBUTE, DataRoutes, ENABLE_DEV_WARNINGS, ErrorBoundary (+23 more))
- **RouteContext** (`packages/react-router/lib/context.ts`): UI_COMPONENT (deps: Await, Book, CRITICAL_CSS_DATA_ATTRIBUTE, DataRoutes, ENABLE_DEV_WARNINGS, ErrorBoundary (+23 more))
- **RouteErrorContext** (`packages/react-router/lib/context.ts`): UI_COMPONENT (deps: Await, Book, CRITICAL_CSS_DATA_ATTRIBUTE, DataRoutes, ENABLE_DEV_WARNINGS, ErrorBoundary (+23 more))
- **RouteIdContext** (`packages/react-router/lib/context.ts`): UI_COMPONENT (deps: Await, Book, CRITICAL_CSS_DATA_ATTRIBUTE, DataRoutes, ENABLE_DEV_WARNINGS, ErrorBoundary (+23 more))
- **ViewTransitionContext** (`packages/react-router/lib/context.ts`): UI_COMPONENT (deps: Await, Book, CRITICAL_CSS_DATA_ATTRIBUTE, DataRoutes, ENABLE_DEV_WARNINGS, ErrorBoundary (+23 more))
- **RemixRootDefaultHydrateFallback** (`packages/react-router/lib/dom/ssr/fallback.tsx`): UI_COMPONENT (deps: Await, Book, BoundaryShell, CRITICAL_CSS_DATA_ATTRIBUTE, DataRoutes, ENABLE_DEV_WARNINGS (+22 more))


## CI/CD Pipeline Topology

```mermaid
graph TD;
  NoWorkflows[No Workflows Detected]
```
