# Domain Setup Guide

## Step 1: Purchase a Domain Name
1. Choose a domain registrar (NameSilo recommended for competitive pricing and reliability)
2. Purchase your desired domain name (e.g., 'my-domain.com')
3. Initially, the domain will use NameSilo's default nameservers:
   - NS1.DNSOWL.COM
   - NS2.DNSOWL.COM 
   - NS3.DNSOWL.COM

You can verify the current nameservers by running: `whois my-domain.com`

## Step 2: Configure Domain on Linode
1. Navigate to Linode's domain creation page:
   https://cloud.linode.com/domains/create
   
2. Fill out the domain creation form
   - Enter your domain name
   - Leave "Insert Default Records" unchecked
   
3. Update Nameservers:
   - Copy the three Linode nameservers provided for your domain
   - Go to NameSilo's domain management panel
   - Replace the default nameservers with Linode's nameservers

From now on, those Linode nameservers will be the ones handling your domain's DNS records (translating domain names into IP addresses,...). 

4. Create new Linode
   - Navigate to https://cloud.linode.com/linodes/create
   - Choose a region close to your target users
   - Select a plan based on your needs (Shared CPU is fine for most sites)
   - Choose Arch Linux as the Linux distribution
   - Set a strong root password or add ssh key for access
   - Click "Create Linode" and wait for provisioning
   - Note down the assigned IP address

Right now, you have a running Linode instance. If you run the command `lsblk`, you can see it has a root partition (sda) and a swap partition. For better organization and scalability, we should create additional block storage:

5. Create a new Block Storage Volume:
   - Go to https://cloud.linode.com/volumes/create
   - Select the same region as your Linode
   - Choose desired size (e.g., 20GB)
   - Attach it to your Linode instance
   - Note down the device path (e.g., /dev/sdb)

6. Format and mount the new volume:

Follow the formatting and mounting instructions displayed in the Block Storage configuration panel. These commands will typically include:
- Creating a filesystem on the volume
- Creating a mount point directory
- Mounting the volume
- Adding an entry to /etc/fstab for persistent mounting, so it would survives rebooting
- run 'lsblk' now and you can see the difference

5. 
