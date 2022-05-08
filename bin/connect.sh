# ! /bash/bin

#43.138.213.29 hadoop01
#43.138.182.180 hadoop02
#43.138.217.253 hadoop03

# lh132137,
echo "please input number:"

echo "1.root@43.138.213.29"
echo "2.root@43.138.182.180"
echo "3.root@43.138.217.253"
read -t 30 -p "please select ip:" ip_num
if [ $ip_num = "1" ];then
    ssh root@43.138.213.29
fi
if [ $ip_num = "2" ];then
    ssh root@43.138.182.180
fi
if [ $ip_num = "3" ];then
    ssh root@43.138.217.253
fi
