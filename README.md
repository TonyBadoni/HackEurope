
ssh -> produces a new .json file with all logs

running server on the honeypod would constantly(every 5 mins) check whether the logs.json was changed, if yes it sends the info 
to the agent through TCP(probably a bad idea), then the agent would react on the data recieved and would run the pipeline
