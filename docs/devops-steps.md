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

## Step 5: Install Ansible

1. Create an ansible directory in your project:
   ```bash
   cd your-project-path
   mkdir ansible
   ```

2. Install Ansible in your virtual environment:
   ```bash
   # Activate virtual environment
   source .venv/Scripts/activate
   
   # Install ansible and update requirements
   pip install ansible
   pip freeze >> requirements.txt
   ```
3. Create ansible.cfg inside /ansible:
   ```ini
   [main]
   black-pig.top
   ```

4. Create setup.yml inside /ansible:
   ```yaml
   - name: Configure server
     hosts: main
     become: yes
     roles:
       - common
       - web
       - db
   ```

## Step 6: Ansible Roles

1. Create the hostname role directory and tasks:
   ```bash
   cd ansible/
   mkdir -p hostname/tasks
   touch hostname/tasks/main.yml
   ```

2. Add the following content to `hostname/tasks/main.yml`:
   ```yaml
   - name: Set hostname
     ansible.builtin.hostname:
       name: vps.black-pig.com
       use: systemd

   - name: Configure localhost in /etc/hosts
     ansible.builtin.hostname:
       path: /etc/hosts
       line: 127.0.0.1 localhost.localmain localhost

   - name: Configure VPS hostname in /etc/hosts
     ansible.builtin.hostname:
       path: /etc/hosts
       line: your-linode-ip-address vps.black-pig.com vps
   ```

3. Update `setup.yml` to include the hostname role:
   ```yaml
   - hosts: main
     roles:
       - hostname
   ```

4. Run the playbook from your local machine:
   ```bash
   cd /ansible
   ansible-playbook setup.yml
   ```

After running the playbook, SSH into your Linode instance and you'll see the hostname has been changed.

Note: It's important to change the hostname from localhost because many services (especially email services) will reject connections from servers using localhost as their hostname.
