#! /usr/bin/env python

import polib, os, sys, argparse

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

        if set(old_msg.flags) != set(new_msg.flags):
            identical = False

        if not identical:
            changed.append({'old':old_msg, 'new':new_msg})

    # metadata
    added_metadata_keys = set(new_pofile.metadata) - set(old_pofile.metadata)
    deleted_metadata_keys = set(old_pofile.metadata) - set(new_pofile.metadata)
    common_metadata_keys = set(old_pofile.metadata) & set(new_pofile.metadata)

    changed_metadata = []
    for common in common_metadata_keys:
        old_metadata = old_pofile.metadata[common]
        new_metadata = new_pofile.metadata[common]

        if old_metadata != new_metadata:
            changed_metadata.append({'key': common, 'old':old_metadata, 'new':new_metadata})


    return {
        'added':[new_msgs[x] for x in added_msgs], 'deleted':[old_msgs[x] for x in deleted_msgs], 'changed':changed,
        'added_metadata_keys': [x for x in new_pofile.metadata.items() if x[0] in added_metadata_keys],
        'deleted_metadata_keys': [x for x in old_pofile.metadata.items() if x[0] in deleted_metadata_keys],
        'changed_metadata': changed_metadata,
    }

    
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
            print "\tmsgstr old: %r\n\t       new: %r" % (old.msgstr, new.msgstr)
        if old.msgstr_plural != new.msgstr_plural:
            print "\tmsgstr_plural old: %r\n\tnew: %r" % (old.msgstr_plural, new.msgstr_plural)

        added_flags = set(new.flags) - set(old.flags)
        deleted_flags = set(old.flags) - set(new.flags)
        if len(added_flags) > 0:
            print "\tAdded flags: %s" % (",".join(sorted(added_flags)))
        if len(deleted_flags) > 0:
            print "\tDelete flags: %s" % (",".join(sorted(deleted_flags)))


    for key, value in diff['added_metadata_keys']:
        print "New metadata: %r: %r" % (key, value)

    for key, value in diff['deleted_metadata_keys']:
        print "Deleted metadata: %r: %r" % (key, value)

    for key in diff['changed_metadata']:
        print "Changed metadata: %r" % key['key']
        print "\told: %r" % key['old']
        print "\tnew: %r" % key['new']


    diff_keys = ['added', 'deleted', 'changed', 'added_metadata_keys', 'deleted_metadata_keys', 'changed_metadata']
    if all(len(diff[key]) == 0 for key in diff_keys):
        print "pofiles are semantically identical"


def exit_code(diff):
    diff_keys = ['added', 'deleted', 'changed', 'added_metadata_keys', 'deleted_metadata_keys', 'changed_metadata']
    return 0 if all(len(diff[key]) == 0 for key in diff_keys) else 1

def main():
    parser = argparse.ArgumentParser()
    #parser.add_argument('--no-ignore-comments')

    parser.add_argument('old_file')
    parser.add_argument('new_file')
    args = parser.parse_args()

    diffs = podiff(polib.pofile(args.old_file), polib.pofile(args.new_file))

    pprint_diff(diffs)
    return exit_code(diffs)


if __name__ == '__main__':
    sys.exit(main())
        
