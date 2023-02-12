docker build -t api_gateway ../api_gateway
docker build -t emb_to_txt ../emb_to_txt

docker run -d -p 5000:5000 --restart=always --name registry registry:2

docker pull tensorflow/serving:2.6.0

docker tag api_gateway 167.235.136.60:5000/api_gateway
docker push 167.235.136.60:5000/api_gateway

docker tag emb_to_txt 167.235.136.60:5000/emb_to_txt
docker push 167.235.136.60:5000/emb_to_txt
