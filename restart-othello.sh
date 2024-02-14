#!/bin/bash

sudo systemctl restart othello
sudo systemctl enable othello
sudo systemctl status othello
sudo systemctl reload nginx

echo "Othello has been restarted"

#xxx