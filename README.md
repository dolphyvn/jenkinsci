# jenkinsci
This python code will detect which commit according from svn repository and auto create standard script, checkout the repo to local server and push it to your environment

This tool seperates in two parts, client and server. The post-commit hook will call the server api which runing bottle framework to received data pass when a commit to svn.

