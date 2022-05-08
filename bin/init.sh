# !/bin/bash


#declare -A ipMap

#ipMap["43.138.213.29"]="lh132137,"
#ipMap["43.138.182.180"]="lh132137,"
#ipMap["43.138.217.253"]="lh132137,"

ip_lst="43.138.213.29 43.138.182.180 43.138.217.253"

for key in $ip_lst;do
    echo $key
    #sshpass -plh132137, ssh root@$key "mkdir -p /opt/software"
    #sshpass -plh132137, ssh root@$key "mkdir -p /opt/module"
    #sshpass -plh132137, ssh root@$key "ls /opt/software"
    #sshpass -plh132137, ssh root@$key "ls /opt"
    #sshpass -plh132137, ssh root@$key "tar -zxvf /opt/software/jdk-8u221-linux-x64.tar.gz -C /opt/module/"
    #sshpass -plh132137, ssh root@$key "touch /etc/profile.d/my_env.sh"
    #sshpass -plh132137, ssh root@$key "echo export JAVA_HOME=/opt/module/jdk1.8.0_221 >> /etc/profile.d/my_env.sh"
    #sshpass -plh132137, ssh root@$key "echo PATH=$PATH:$JAVA_HOME/bin >> /etc/profile.d/my_env.sh"
    #sshpass -plh132137, ssh root@$key "source /etc/profile"
    #sshpass -plh132137, ssh root@$key "tar -zxvf /opt/software/hadoop-3.1.3.tar.gz -C /opt/module/"
    #sshpass -plh132137, ssh root@$key "ls /opt/module/"
    #sshpass -plh132137, ssh root@$key "echo export HADOOP_HOME=/opt/module/hadoop-3.1.3 > /etc/profile.d/my_env.sh"
    #sshpass -plh132137, ssh root@$key "echo export PATH=$PATH:$HADOOP_HOME/bin >> /etc/profile.d/my_env.sh"
    #sshpass -plh132137, ssh root@$key "echo export PATH=$PATH:$HADOOP_HOME/sbin >> /etc/profile.d/my_env.sh"
    #sshpass -plh132137, ssh root@$key "source /etc/profile"
    #sshpass -plh132137, ssh root@$key "ls /opt/module/"
    #sshpass -plh132137, ssh root@$key "java -version"
    #sshpass -plh132137, ssh root@$key "hadoop version"

    sshpass -plh132137, ssh root@$key "ls /opt/module/hadoop-3.1.3"
done
