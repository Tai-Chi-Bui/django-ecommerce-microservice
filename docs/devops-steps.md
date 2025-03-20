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


