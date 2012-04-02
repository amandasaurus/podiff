#! /usr/bin/env python

import polib, os, sys

def podiff(old_pofile, new_pofile):
    # TODO support context
    old_msgs = dict(((entry.msgid, entry.msgid_plural), entry) for entry in old_pofile)
    new_msgs = dict(((entry.msgid, entry.msgid_plural), entry) for entry in new_pofile)

    added_msgs = set(new_msgs.keys()) - set(old_msgs.keys())
    deleted_msgs = set(old_msgs.keys()) - set(new_msgs.keys())
    common_msgs = set(old_msgs.keys()) & set(new_msgs.keys())

    changed = []
    for common in common_msgs:
        old_msg = old_msgs[common]
        new_msg = new_msgs[common]

        identical = True
        for attr in ['msgid', 'msgid_plural', 'msgstr']:
            if getattr(old_msg, attr) != getattr(new_msg, attr):
                identical = False

        if not identical:
            changed.append({'old':old_msg, 'new':new_msg})



    return {'added':[new_msgs[x] for x in added_msgs], 'deleted':[old_msgs[x] for x in deleted_msgs], 'changed':changed}

    
def _repr_msg(msg):
    if msg.msgid_plural == '':
        return '%r' % msg.msgid
    else:
        return '%r/%r' % (msg.msgid, msg.msgid_plural)

def pprint_diff(diff):
    if len(diff['added']) > 0:
        for msg in diff['added']:
            if msg.msgid_plural == '':
                print "New msg: msgid=%r msgstr=%r" % (msg.msgid, msg.msgstr)
            else:
                print "New msg: msgid=%r/%r msgstr=%r" % (msg.msgid, msg.msgid_plural, msg.msgstr)

    if len(diff['deleted']) > 0:
        for msg in diff['deleted']:
            if msg.msgid_plural == '':
                print "Deleted msg: msgid=%r msgstr=%r" % (msg.msgid, msg.msgstr)
            else:
                print "Deleted msg: msgid=%r/%r msgstr=%r" % (msg.msgid, msg.msgid_plural, msg.msgstr)

    for msg in diff['changed']:
        old, new = msg['old'], msg['new']
        change = ""
        print "Changed msg: %s" % _repr_msg(old)
        if old.msgstr != new.msgstr:
            print "\tmsgstr old: %r new: %r" % (old.msgstr, new.msgstr)
        if old.msgstr_plural != new.msgstr_plural:
            print "\tmsgstr_plural old: %r new: %r" % (old.msgstr_plural, new.msgstr_plural)

    if len(diff['added']) == 0 and len(diff['deleted']) == 0 and len(diff['changed']) == 0:
        print "pofiles are semantically identical"


def exit_code(diff):
    if len(diff['added']) == 0 and len(diff['deleted']) == 0 and len(diff['changed']) == 0:
        return 0
    else:
        return 1

def main(argv):
    old, new = argv
    diffs = podiff(polib.pofile(old), polib.pofile(new))
    pprint_diff(diffs)
    return exit_code(diffs)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
        
