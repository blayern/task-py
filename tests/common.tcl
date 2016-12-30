#!/usr/bin/expect

set timeNow [clock seconds]
set logFile [open "./results/logfile-[clock format $timeNow -format %Y-%M-%d-%H-%M-%S].txt" w+]

proc logResult {step result {msg {}}} {
	global logFile
	if {$step==""} {set str ""
	} else {set str "Step "}
	puts "$str$step: $result $msg"
	puts $logFile "$str$step: $result $msg"
}

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

