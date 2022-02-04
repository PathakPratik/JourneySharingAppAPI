FROM nginx
RUN rm /etc/nginx/nginx.conf /etc/nginx/conf.d/default.conf
COPY wait-for-it.sh wait-for-it.sh
RUN chmod +x wait-for-it.sh
# CMD ["/wait-for-it.sh", "app:5011", "--", "nginx", "-g", "daemon off;"]
CMD [ "./wait-for-it.sh", "userapi:5000", "--",  "nginx", "-g", "daemon off;" ]
ADD conf /etc/nginx