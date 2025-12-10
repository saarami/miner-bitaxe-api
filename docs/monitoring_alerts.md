# Monitoring & Alerts (planned)

Planned alert conditions:

- Miner overheating (core temperature above a configured threshold)
- Miner offline (no successful poll for N minutes)
- Hash rate below a configured threshold
- High rejected share ratio

Planned Telegram integration:

- Use a Telegram bot token and chat ID stored in environment variables
- Send a short alert message with timestamp and key metrics
