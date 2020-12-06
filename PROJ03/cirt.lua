-- CIRT Wireshark Dissector
-- Kevin Scrivnor, Spring 2020
cirt_proto = Proto("CIRT", "CI Reliable Transport")

seqno = ProtoField.int32("cirt.sequence_number", "sequence number: ", base.DEC)
ackno = ProtoField.int32("cirt.acknowledgement_number", "acknowledgement number: ", base.DEC)
win = ProtoField.int16("cirt.window_size", "window size: ", base.DEC)
unused = ProtoField.int8("cirt.unused", "unused: ", base.DEC)
flags = ProtoField.int8("cirt.flags", "flags: ", base.DEC)

cirt_proto.fields = { seqno, ackno, win, unused, flags }
-- function to dissect
function cirt_proto.dissector(buffer,pinfo,tree)
    length = buffer:len()
    if length == 0 then return end
    
    pinfo.cols.protocol = "CIRT"
    local subtree = tree:add(cirt_proto,buffer(),"CIRT Data")

    subtree:add(seqno, buffer(0,4))
    subtree:add(ackno, buffer(4,4))
    subtree:add(win, buffer(8,2))
    subtree:add(unused, buffer(10,1))

    local flag = buffer(11,1):uint()
    local flag_str = get_flag_type(flag)
    subtree:add(flags, buffer(11,1)):append_text(" (" .. flag_str .. ")")
end
-- function for dealing with the flags
function get_flag_type(flag)
    local flag_str = "UNKNOWN"

    if flag == 0 then flag_str = "NONE"
    elseif flag == 1 then flag_str = "SYN"
    elseif flag == 2 then flag_str = "ACK"
    elseif flag == 3 then flag_str = "SYNACK"
    elseif flag == 4 then flag_str = "FIN"
    elseif flag == 8 then flag_str = "ERR" end

    return flag_str
end
-- register the protocol on UDP port 9001 (default CIRT port)
udp_table = DissectorTable.get("udp.port")
udp_table:add(9001,cirt_proto)