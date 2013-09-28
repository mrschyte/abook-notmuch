from notmuch import Query, Database
import email.header
import re

def export_abook(addresses):
    print("[format]\nprogram=abook\nversion=0.6.0.pre2")

    for idx, (key, val) in enumerate(addresses.items()):
        print("\n[%d]\nname=%s\nemail=%s" % (idx, val, key))


def proc_header(msg, field):
    header = msg.get_header(field)
    dec = email.header.decode_header(header)

    if type(dec[0][0]) == bytes and dec[0][1] != None:
        dec[0] = (dec[0][0].decode(dec[0][1]), None)

    if type(dec[0][0]) != bytes:
        for address in re.split(', +', dec[0][0]):
            fields = re.split(' +<', address.replace('"','').replace("'",""))
            if len(fields) == 2 \
                and len(fields[0]) > 0 and len(fields[1]) > 0:
                return (fields[1][:-1], fields[0])
    return None

def grab_addresses(msgs):
    addresses = {}
    for msg in msgs:
        res = proc_header(msg, "from")
        if res != None:
            addresses[res[0]] = res[1]

        res = proc_header(msg, "to")
        if res != None:
            addresses[res[0]] = res[1]

        res = proc_header(msg, "cc")
        if res != None:
            addresses[res[0]] = res[1]

    return addresses

db = Database(None, create=False)
msgs = Query(db, 'tag:inbox or tag:archive').search_messages()

addresses = {}

addresses.update(grab_addresses(msgs))

export_abook(addresses)
