# Generating a GitHub Personal Access Token (PAT)

Atruss Code Atlas leverages the GitHub REST API to perform massive, asynchronous sweeps of organizational structures. While this API technically allows unauthenticated access for public repositories, GitHub natively enforces an extremely strict rate limit of **60 requests per hour** for anonymous users. 

Because the analyzer pulls extensive paginated workflow, runner, environment, and repository trees concurrently, scanning any moderately sized organization will exhaust this unauthenticated rate limit within seconds. Providing a Personal Access Token immediately raises your limit to **5,000 requests per hour**.

Here is how you generate a lightweight, secure token.

---

### Step 1: Navigate to Developer Settings
1. Log in to your personal GitHub account at **[github.com](https://github.com)**.
2. Click your **profile photo** in the top right corner and select **Settings**.
3. Scroll all the way down the left sidebar and click **< > Developer settings**.

### Step 2: Generate the Token
1. In the left sidebar, click **Personal access tokens**, then select **Tokens (classic)**.
2. Click the **Generate new token** button (select **Generate new token (classic)** if prompted).
3. *Note: GitHub may securely prompt you to confirm your password or use two-factor authentication.*

### Step 3: Configure the Token Scopes
1. **Name**: Give your token a descriptive name, like `Atruss Code Atlas API`.
2. **Expiration**: Choose how long you want the token to last (e.g., 30 days is a safe default).
3. **Select scopes**: 
   - **For Public Repositories Only**: You technically **do not need to check any boxes at all**. Leaving all scopes empty generates a generic "Public Access" token that safely bumps your API rate limit to 5,000 requests per hour without risking write-access to your account.
   - **For Private Repositories**: If you ever want the analyzer to scan your own private enterprise repositories, you must check the `repo` *(Full control of private repositories)* box here.

### Step 4: Save and Export
1. Scroll to the bottom and click **Generate token**.
2. **Copy the token immediately!** (It starts with `ghp_...`). GitHub will never show it to you again once you leave this page.
3. Keep it secure and feed it into your execution environment.

---

## Usage in Atruss Code Atlas

You can pass the token directly to the CLI commands, but we recommend exporting it as an environment variable to prevent it from saving in your local bash history:

**On Windows (PowerShell):**
```powershell
$env:GH_TOKEN="ghp_YourCopiedTokenHere..."
repo-analyzer discover --org some-public-org
```

**On macOS/Linux:**
```bash
export GH_TOKEN="ghp_YourCopiedTokenHere..."
repo-analyzer discover --org some-public-org
```
