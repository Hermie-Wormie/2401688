FROM nginxinc/nginx-unprivileged:1.27-alpine
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY html/ /usr/share/nginx/html/
COPY --chown=nginx:nginx certs/ /etc/nginx/certs/
EXPOSE 8080 8443
CMD ["nginx", "-g", "daemon off;"]