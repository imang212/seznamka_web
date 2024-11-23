#!/bin/bash
git pull origin main --rebase
git add .
git commit -m "Automatická aktualizace"
git push origin main