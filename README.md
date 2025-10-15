# Job Board Monitor

Automatically monitors the Switchyards job board for changes and notifies you via GitHub Actions.

## Setup Instructions

### 1. Push to GitHub
```bash
git init
git add .
git commit -m "Initial commit: Job board monitor"
git remote add origin <your-github-repo-url>
git push -u origin main
```

### 2. Configure Email Notifications

You'll need to set up GitHub Secrets for email notifications:

1. Go to your GitHub repository
2. **Settings → Secrets and variables → Actions**
3. Click **New repository secret** and add these three secrets:

   - `MAIL_USERNAME`: Your email address (e.g., `yourname@gmail.com`)
   - `MAIL_PASSWORD`: Your email app password (see below)
   - `MAIL_TO`: Email where you want notifications sent (can be same as username)

**Getting a Gmail App Password:**
1. Go to your Google Account → Security
2. Enable 2-Step Verification if not already enabled
3. Search for "App passwords" 
4. Generate a new app password for "Mail"
5. Use this 16-character password as `MAIL_PASSWORD`

**Alternative Email Providers:**
If you're not using Gmail, modify the workflow file:
- **Outlook/Hotmail**: `smtp.office365.com`, port `587`
- **Yahoo**: `smtp.mail.yahoo.com`, port `587`
- **Custom SMTP**: Update server_address and server_port accordingly

### 3. Enable GitHub Actions
The workflow will automatically run daily at 9 AM CT (3 PM UTC). The schedule is already configured in `.github/workflows/monitor.yml`.

To change the schedule, edit the cron expression:
- Current: `0 15 * * *` (9 AM Central = 3 PM UTC)
- Every 6 hours: `0 */6 * * *`
- Twice daily (9 AM & 5 PM CT): `0 15,23 * * *`

### 4. First Run
Run the workflow manually to establish a baseline:
1. Go to **Actions** tab in your repo
2. Click **Job Board Monitor** workflow
3. Click **Run workflow**
4. This creates the initial hash file

## How It Works

1. **Python script** (`job_monitor.py`) fetches the job board and creates a hash of the content
2. **GitHub Actions** runs the script on a schedule
3. If content changes, the job "fails" (exits with code 1)
4. GitHub Actions sends you an email notification
5. The hash file is committed back to the repo to track changes between runs

## Customization

### Change check frequency
Edit `.github/workflows/monitor.yml` cron schedule:
- Every 6 hours: `0 */6 * * *`
- Twice daily (9 AM & 5 PM CT): `0 15,23 * * *`
- Weekdays only at 9 AM CT: `0 15 * * 1-5`

Note: GitHub Actions uses UTC time. Central Time = UTC - 6 (or -5 during DST)

### Filter for Nashville jobs only
Modify `job_monitor.py` to parse the HTML and only hash Nashville-specific content:
```python
from bs4 import BeautifulSoup

def filter_nashville_jobs(content):
    soup = BeautifulSoup(content, 'html.parser')
    # Extract only Nashville job listings
    # This depends on the page structure
    return str(soup)
```

## Troubleshooting

- **Workflow fails immediately**: Check if the URL is accessible and secrets are set correctly
- **No email notifications**: Verify your email secrets (MAIL_USERNAME, MAIL_PASSWORD, MAIL_TO) are correct
- **Gmail not working**: Make sure you're using an App Password, not your regular password
- **Workflow not running on schedule**: Check the Actions tab to see if workflows are enabled

## Alternative: No Email Setup Required

If you don't want to set up email, you can still get notifications:

1. **GitHub Mobile App**: Enable push notifications for workflow failures
2. **Watch the repo**: Settings → Watch → Custom → Check "Actions"
3. **GitHub Email**: You'll get emails about failed workflows automatically (no secrets needed)

Just remove or comment out the "Send email notification" step in the workflow file.

## Files

- `job_monitor.py` - Main monitoring script
- `.github/workflows/monitor.yml` - GitHub Actions workflow
- `requirements.txt` - Python dependencies
- `job_board_hash.txt` - Cached hash (auto-generated and committed)
