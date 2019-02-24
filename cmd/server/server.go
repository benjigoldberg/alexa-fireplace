package server

import (
	"github.com/benjigoldberg/alexa-fireplace/pkg/server"
	"github.com/spf13/cobra"
)

const longDescription = `
Runs a Server for controlling the fireplace
`

// NewCmd constructs a cobra command for running a spotbot server
func NewCmd(gitSHA string) *cobra.Command {
	c := server.Config{}
	cmd := &cobra.Command{
		Use:   "server",
		Short: "Runs a Server for controlling the fireplace",
		Long:  longDescription,
		RunE: func(cmd *cobra.Command, args []string) error {
			c.Server.RunHTTPServer(c.PreStart, nil, c.RegisterMuxes)
			return nil
		},
	}

	// Server Config
	flags := cmd.Flags()
	c.RegisterFlags(flags, "fireplace", gitSHA)
	return cmd
}
