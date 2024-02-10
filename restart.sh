#!/bin/bash

# This script is used to restart the server
sudo systemctl daemon-reload
sudo systemctl start othello
sudo systemctl enable othello
sudo systemctl status othello
```