#!/bin/zsh

script_dir='/Library/UWEC/scripts/jamf_ip_scraper'
log_dir='/Library/UWEC/scripts/log/jamf_ip_scraper'
date=$(/bin/date +%Y.%m.%d)

# Make sure logging directory exists, and if not, create it
if [ ! -d $log_dir ]; then
  /bin/mkdir -p $log_dir
fi

# Run the script
source "${script_dir}"/venv/bin/activate
"${script_dir}"/venv/bin/python3 "${script_dir}"/main.py &> $log_dir/"${date}"_jamf_ip_scraper.log
deactivate