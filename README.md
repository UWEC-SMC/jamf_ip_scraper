# Jamf IP Scraper

After being burned one too many times by Jamf making opaque changes to their outbound cloud traffic, I got fed up and wrote a script that scrapes their [article outlining their outbound IPs/Domains](https://learn.jamf.com/bundle/technical-articles/page/Permitting_InboundOutbound_Traffic_with_Jamf_Cloud.html) and 
converts it into an easily digested JSON file ([jamf_outbound_traffic.json](https://raw.githubusercontent.com/UWEC-SMC/jamf_ip_scraper/main/jamf_outbound_traffic.json)). This has the advantage of not only allowing admins the ability to progmatically process these values, but also provides an easily understood change log. 
