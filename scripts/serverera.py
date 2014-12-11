import subprocess


###
# Server Specs
###
cpu = subprocess.check_output("awk -F: '/model name/ {name=$2;} END {print name;}' /proc/cpuinfo", shell=True)
cores = subprocess.check_output("awk -F: '/model name/ {core++} END {print core}' /proc/cpuinfo", shell=True)
freq = subprocess.check_output("awk -F: '/cpu MHz/ {freq=$2} END {print freq}' /proc/cpuinfo", shell=True)
ram = subprocess.check_output("free -m | awk 'NR==2 {print $2}'", shell=True)

print "\nServerEra Benchmarking Script"
print "CPU model: %s" % cpu.strip()
print "Number of cores: %s" % cores.strip()
print "CPU frequency: %s MHz" % freq.strip()
print "RAM: %s MB" % ram.strip()


###
# Disk Performance Tests
###
print "\nRunning Disk Performance Tests..."
disk = subprocess.check_output("(dd bs=1M count=1024 if=/dev/zero of=outfile conv=fdatasync) 2>&1 | awk -F, '{io=$NF} END { print io}'", shell=True)
subprocess.call("rm outfile", shell=True)
disk = disk.strip()
print "Disk Speed: %s" % disk


###
# Bandwidth Performance Tests
###
print "\nRunning Bandwidth Performance Tests"
servers = [
    {
        "name": "Cachefly",
        "location": "CDN",
        "url": "http://cachefly.cachefly.net/100mb.test"
    },
    {
        "name": "DigitalOcean",
        "location": "New York, USA",
        "url": "http://ipv4.speedtest-nyc3.digitalocean.com/100mb.test"
    },
    {
        "name": "Softlayer",
        "location": "San Jose, USA",
        "url": "http://speedtest.sjc01.softlayer.com/downloads/test100.zip"
    },
    {
        "name": "Linode",
        "location": "London, UK",
        "url": "http://speedtest.london.linode.com/100MB-london.bin"
    },
    {
        "name": "LeaseWeb",
        "location": "Amsterdam, NL",
        "url": "http://mirror.nl.leaseweb.net/speedtest/100mb.bin"
    },
    {
        "name": "DigitalOcean",
        "location": "Singapore",
        "url": "http://ipv4.speedtest-sgp1.digitalocean.com/100mb.test"
    },
    {
        "name": "Linode",
        "location": "Tokyo, Japan",
        "url": "http://speedtest.tokyo.linode.com/100MB-tokyo.bin"
    },
]

for server in servers:
    print "Downloading from %s - %s ..." % (server['name'], server['location'])
    speed = subprocess.check_output("wget -O /dev/null %s 2>&1" % server['url'], shell=True)

    speed = speed.strip()
    speed = speed.split('\n')
    speed_split = speed[-1].split()
    result = "%s %s" % (speed_split[2], speed_split[3])
    result = result[1:-1]

    print "Network speed: %s" % result
