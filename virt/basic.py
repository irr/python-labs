#!/usr/bin/python -u
import libvirt
import sys

conn = libvirt.open("vbox:///session")

if conn == None:
    print 'Failed to open connection to the hypervisor'
    sys.exit(1)

# print conn

try:
    dom0 = conn.lookupByName("Ubuntu")
except:
    print 'Failed to find the main domain'
    sys.exit(1)

# print dom0

print "Domain 0: id %d %s" % (dom0.ID(), dom0.OSType())
print dom0.info()

xml = """
<domain type='vbox'>
  <name>Ubuntu2</name>
  <uuid>20930c01-af06-4419-ae0a-01d18535371c</uuid>
  <memory>262144</memory>
  <currentMemory>262144</currentMemory>
  <vcpu>1</vcpu>
  <os>
    <type arch='i686'>hvm</type>
    <boot dev='fd'/>
    <boot dev='cdrom'/>
    <boot dev='hd'/>
  </os>
  <features>
    <acpi/>
  </features>
  <clock offset='localtime'/>
  <on_poweroff>destroy</on_poweroff>
  <on_reboot>destroy</on_reboot>
  <on_crash>destroy</on_crash>
  <devices>
    <disk type='file' device='disk'>
      <source file='/home/irocha/VirtualBox VMs/Ubuntu2/Ubuntu2.vdi'/>
      <target dev='sda' bus='sata'/>
    </disk>
    <interface type='user'>
      <mac address='08:00:27:19:c3:c9'/>
      <model type='82540EM'/>
    </interface>
    <input type='mouse' bus='ps2'/>
    <graphics type='desktop' display=':0.0'/>
    <sound model='ac97'/>
    <video>
      <model type='vbox' vram='12288' heads='1'>
        <acceleration accel3d='no' accel2d='no'/>
      </model>
    </video>
  </devices>
</domain>
"""

# dom0.create()

dom1 = conn.createXML(xml, 0)

del dom0
del conn

print "OK"

sys.exit(0)
