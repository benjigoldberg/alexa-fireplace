package main

import (
	"os"

	"github.com/benjigoldberg/alexa-fireplace/cmd/server"
	"github.com/spf13/cobra"
	"github.com/spothero/tools"
)

// This should be set during build with the Go link tool
// e.x.: when running go build, provide -ldflags="-X main.gitSHA=<GITSHA>"
var gitSHA = "not-set"

func newRootCmd(args []string) *cobra.Command {
	cmd := &cobra.Command{
		Use:              "fireplace",
		Short:            "Provides fireplace controls via Raspberry Pi GPIO",
		Long:             `Provides fireplace controls via Raspberry Pi GPIO.`,
		Version:          gitSHA,
		PersistentPreRun: tools.CobraBindEnvironmentVariables("fireplace"),
	}
	cmd.AddCommand(server.NewCmd(gitSHA))
	return cmd
}

func main() {
	if err := newRootCmd(os.Args[1:]).Execute(); err != nil {
		os.Exit(1)
	}
}
