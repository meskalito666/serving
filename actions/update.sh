# делаем последовательный апдейт и заменяем переменную среды, которая отвечает за директорию с нужным поколением индекстов 
docker service update --update-delay 15s --update-failure-action=rollback --env-add VERSION=idx_2 service_emb_to_txt_0
docker service update --update-delay 15s --update-failure-action=rollback --env-add VERSION=idx_2 service_emb_to_txt_1
docker service update --update-delay 15s --update-failure-action=rollback --env-add VERSION=idx_2 service_emb_to_txt_2
docker service update --update-delay 15s --update-failure-action=rollback --env-add VERSION=idx_2 service_emb_to_txt_3

docker service update --update-delay 15s --update-failure-action=rollback --env-add VERSION=idx_2 service_api_gateway