FROM rowsheet/public_docker_base:v0.0.1

# Note: You must change this in the both:
# 	1) CONFIG.json
#	2) Dockerfile
EXPOSE 9999

#-------------------------------------------------------------------------------
# Common: Docker entrypoint.
#-------------------------------------------------------------------------------
#	Run the entry point and provide it a command so the container doesn't 
#	immidiatley exit.
COPY ENTRYPOINT.sh /usr/local/bin/
RUN ln -s /usr/local/bin/ENTRYPOINT.sh / # backwards compat
ENTRYPOINT ["sh", "/ENTRYPOINT.sh"]
#	The command doesn't really matter, but you have to pass it something.
CMD ["EXAMPLE"]
