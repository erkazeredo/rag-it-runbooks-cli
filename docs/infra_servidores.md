# Runbook: Reinicialização de Serviços Críticos e Banco de Dados

## Alerta de Alto Consumo de CPU no Servidor PostgreSQL (`db-prod-01`)
Quando o monitoramento Zabbix disparar alerta de CPU acima de 90% por mais de 10 minutos no servidor `db-prod-01`:
1. Acesse o servidor via SSH utilizando a conta de serviço `ops_admin`.
2. Identifique consultas travadas rodando `SELECT pid, now() - query_start AS duration, query FROM pg_stat_activity WHERE state != 'idle' ORDER BY duration DESC;`.
3. Encerre apenas consultas com duração superior a 15 minutos usando `SELECT pg_terminate_backend(PID);`.
4. **Proibição:** Nunca reinicie o serviço principal do PostgreSQL (`systemctl restart postgresql`) em horário comercial sem autorização expressa do Tech Lead de Infraestrutura.