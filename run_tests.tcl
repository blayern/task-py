#!/usr/bin/tclsh

set timeNow [clock seconds]
set logFile [open "./results/logfile-[clock format $timeNow -format %Y-%M-%d-%H-%M-%S].txt" w+]

foreach test [lsort -dictionary [glob -directory tests/ test_*.exp]] {
	set fp [open "$test" r]
	set data [read $fp]
	close $fp
	foreach line [split $data "\r\n"] {
		if {[regexp "set testTitle \"(.*)\"" $line -> testTitle]} {break}
	}
	catch {exec expect $test} output

	if {[string last "PASSED" $output]!=-1} {
		puts "$testTitle - PASSED"
	} elseif {[string first "FAIL" $output]!=-1} {
		foreach line [split $output "\r\n"] {
			if {[regexp "FAIL at step (\[0-9]+) (.*)" $line -> step msg]} {break}
		}
		puts "$testTitle - FAIL at step $step - $msg"
	} else {puts "$testTitle - BUG"}
	puts $logFile "\n###\n$output\n###"
}

close $logFile
