import subprocess


# Write results to this filename
results = open("Results_EtherRank.txt", "w")


###
# Installing required packages for UnixBench
###
# print "\n Installing required packages for UnixBench"
# subprocess.call("sudo apt-get update", shell=True)
# subprocess.call("sudo apt-get install -y libx11-dev libgl1-mesa-dev libxext-dev perl perl-modules make", shell=True)


###
# Server Specs
###
cpu = subprocess.check_output("awk -F: '/model name/ {name=$2;} END {print name;}' /proc/cpuinfo", shell=True)
cores = subprocess.check_output("awk -F: '/model name/ {core++} END {print core}' /proc/cpuinfo", shell=True)
freq = subprocess.check_output("awk -F: '/cpu MHz/ {freq=$2} END {print freq}' /proc/cpuinfo", shell=True)
ram = subprocess.check_output("free -m | awk 'NR==2 {print $2}'", shell=True)

cpu = cpu.strip()
cores = cores.strip()
freq = freq.strip()
ram = ram.strip()

print "\nEtherRank Benchmarking Script"
print "CPU model: %s" % cpu
print "Number of cores: %s" % cores
print "CPU frequency: %s MHz" % freq
print "RAM: %s MB" % ram

results.write("EtherRank Benchmarking Script\n")
results.write("CPU model: %s\n" % cpu)
results.write("Number of cores: %s\n" % cores)
results.write("CPU frequency: %s MHz\n" % freq)
results.write("RAM: %s MB\n" % ram)


###
# dd Disk Performance Tests
###
print "\nRunning dd Disk Performance Tests..."
disk = subprocess.check_output("(dd bs=1M count=1 if=/dev/zero of=outfile conv=fdatasync) 2>&1 | awk -F, '{io=$NF} END { print io}'", shell=True)
subprocess.call("rm outfile", shell=True)
disk = disk.strip()
print "dd Disk Speed: %s" % disk
results.write("dd Disk Speed: %s\n" % disk)


###
# dd CPU Performance Test
###
print "\nRunning dd CPU Performance Tests..."
p = subprocess.Popen("dd bs=1M count=1 if=/dev/zero | md5sum",
                     shell=True,
                     stdout=subprocess.PIPE,
                     stderr=subprocess.PIPE)
out, err = p.communicate()
dd_cpu = err.split(',')[2].strip()
print "dd CPU Speed: %s" % dd_cpu
results.write("dd CPU Speed: %s\n" % dd_cpu)


###
# Bandwidth Performance Tests
###
# print "\nRunning Bandwidth Performance Tests"
# servers = [
#     {
#         "name": "Cachefly",
#         "location": "CDN",
#         "url": "http://cachefly.cachefly.net/100mb.test"
#     },
#     {
#         "name": "DigitalOcean",
#         "location": "New York, USA",
#         "url": "http://ipv4.speedtest-nyc3.digitalocean.com/100mb.test"
#     },
#     {
#         "name": "Softlayer",
#         "location": "San Jose, USA",
#         "url": "http://speedtest.sjc01.softlayer.com/downloads/test100.zip"
#     },
#     {
#         "name": "Linode",
#         "location": "London, UK",
#         "url": "http://speedtest.london.linode.com/100MB-london.bin"
#     },
#     {
#         "name": "LeaseWeb",
#         "location": "Amsterdam, NL",
#         "url": "http://mirror.nl.leaseweb.net/speedtest/100mb.bin"
#     },
#     {
#         "name": "DigitalOcean",
#         "location": "Singapore",
#         "url": "http://ipv4.speedtest-sgp1.digitalocean.com/100mb.test"
#     },
#     {
#         "name": "VULTR",
#         "location": "Tokyo, Japan",
#         "url": "http://hnd-jp-ping.vultr.com/vultr.com.100MB.bin"
#     },
# ]
#
# for server in servers:
#     print "Downloading from %s - %s ..." % (server['name'], server['location'])
#     speed = subprocess.check_output("wget -O /dev/null %s 2>&1" % server['url'], shell=True)
#
#     speed = speed.strip()
#     speed = speed.split('\n')
#     speed_split = speed[-1].split()
#     result = "%s %s" % (speed_split[2], speed_split[3])
#     result = result[1:-1]
#
#     print "Network speed: %s" % result
#     results.write("%s - %s - Network speed: %s\n" % (server['name'], server['location'], result))


###
# UnixBench Performance Test
###
# Change download URL to github location
download_url = "http://byte-unixbench.googlecode.com/files/UnixBench5.1.3.tgz"
subprocess.call("wget -q --no-check-certificate " + download_url, shell=True)
subprocess.call("tar xvf UnixBench5.1.3.tgz", shell=True)
unixbench = subprocess.check_output("cd UnixBench; ./Run -c 1", shell=True)

for item in unixbench.split("\n"):
    if "System Benchmarks Index Score" in item:
        unixbench_score = item.strip().split()[4]
        print "UnixBench Score: %s\n" % unixbench_score
        results.write("UnixBench Score: %s\n" %unixbench_score)

print "\nFINISHED benchmarking script! See Results_EtherRank.txt for results.\n"
