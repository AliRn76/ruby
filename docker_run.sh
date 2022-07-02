docker run -v /srv/ruby/media:/ruby/media -p 8000:8000 --name ruby --network ruby --restart always -d ruby:v1
docker logs -f ruby