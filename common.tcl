#!/usr/bin/expect

proc createTestLine {args} {
	set line ""
	set idx 0
	foreach arg $args {
		if {[lindex $args [expr $idx+1]]!=""} {
			set line ${line}${arg},
		} else {
			set line ${line}${arg}.
		}
		incr idx
	}
	return $line
}

proc createTestFile {args} {
	set fp [open "test.file" w+]
	foreach arg $args {
		puts $fp $arg
	}
	close $fp
}

