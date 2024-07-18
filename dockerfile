# Use the OpenMPI base image
FROM mfisherman/openmpi:latest

# Switch to root user to perform package installation
USER root

# Install Python and necessary packages
RUN apk update && \
    apk add --no-cache python3 py3-pip && \
    pip3 install mpi4py numpy

# Set the working directory
WORKDIR /app

# Copy the Python script into the container
COPY prime.py /app/prime.py

# Set default command to run MPI Python script
CMD ["mpiexec", "-np", "4", "python3", "prime.py"]
