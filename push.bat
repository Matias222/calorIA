git add .

git commit -m "Add: flujo agregar comida por texto e modificacion a la imagen"

git push

aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 441925558343.dkr.ecr.us-east-1.amazonaws.com

docker build -t foodie .

docker tag foodie:latest 441925558343.dkr.ecr.us-east-1.amazonaws.com/foodie:latest

docker push 441925558343.dkr.ecr.us-east-1.amazonaws.com/foodie:latest