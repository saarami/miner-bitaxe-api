# Database Schema – miner_status table

Table name: `miner_status`

| Column          | Type     | Description                           |
|-----------------|----------|---------------------------------------|
| id              | Integer  | Primary key                           |
| timestamp       | DateTime | Record time in UTC                    |
| online          | Boolean  | Miner online (`true`) or offline      |
| hash_rate       | Float    | Hash rate                             |
| temp_core       | Float    | ASIC core temperature (°C)            |
| temp_vr         | Float    | VRM temperature (°C)                  |
| best_difficulty | Float    | Best difficulty reached               |
| shares_accepted | Integer  | Number of accepted shares             |
| shares_rejected | Integer  | Number of rejected shares             |
| frequency       | Float    | ASIC frequency (MHz)                  |
| core_voltage    | Float    | Core voltage (mV)                     |
| raw             | JSONB    | Raw JSON response from the miner      |
