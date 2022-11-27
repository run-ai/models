FROM nvcr.io/nvidia/clara-train-sdk:v3.1.01

# based on https://github.com/kubeflow/mpi-operator/blob/3f808b1c592c767b8d4b60613cad385c7a81dee0/build/base/Dockerfile

RUN apt-get update && apt-get install -y --no-install-recommends \
    openssh-server \
    openssh-client \
    libcap2-bin \
&& rm -rf /var/lib/apt/lists/*

# Add priviledge separation directoy to run sshd as root.
RUN mkdir -p /var/run/sshd
# Add capability to run sshd as non-root.
RUN setcap CAP_NET_BIND_SERVICE=+eip /usr/sbin/sshd

ARG port=22

# Allow OpenSSH to talk to containers without asking for confirmation
# by disabling StrictHostKeyChecking.
# mpi-operator mounts the .ssh folder from a Secret. For that to work, we need
# to disable UserKnownHostsFile to avoid write permissions.
# Disabling StrictModes avoids directory and files read permission checks.
RUN sed -i "s/[ #]\(.*StrictHostKeyChecking \).*/ \1no/g" /etc/ssh/ssh_config \
    && echo "    UserKnownHostsFile /dev/null" >> /etc/ssh/ssh_config \
    && sed -i "s/[ #]\(.*Port \).*/ \1$port/g" /etc/ssh/ssh_config \
    && sed -i "s/#\(StrictModes \).*/\1no/g" /etc/ssh/sshd_config \
    && sed -i "s/#\(Port \).*/\1$port/g" /etc/ssh/sshd_config

RUN echo "PidFile /root/sshd.pid" >> /root/.sshd_config
RUN echo "HostKey /root/.ssh/id_rsa" >> /root/.sshd_config
RUN echo "StrictModes no" >> /root/.sshd_config
RUN echo "Port $port" >> /root/.sshd_config

CMD [ "/bin/bash", "-c", "cp -f ./train_2gpu.sh ./train_2gpu_runai.sh && sed -i 's/-H localhost:2/-x PYTHONPATH/g' ./train_2gpu_runai.sh && ./train_2gpu_runai.sh" ]
