package server

import (
	"context"
	"encoding/json"
	"fmt"
	"net/http"

	"github.com/benjigoldberg/alexa-fireplace/pkg/fireplace"
	"github.com/spf13/pflag"
	"github.com/spothero/tools"
)

// Config wraps the web server configuration
type Config struct {
	Server    tools.HTTPServerConfig
	oAuthConf OAuthConfig
	oAuth     OAuth
}

// RegisterFlags registers flags with pflag driven CLIs
func (c *Config) RegisterFlags(flags *pflag.FlagSet, name, gitSHA string) {
	c.Server.RegisterFlags(
		flags,
		8000,
		name,
		gitSHA,
		"github.com/benjigoldberg/alexa-fireplace",
		gitSHA,
	)
	c.oAuthConf.RegisterFlags(flags)
}

// PreStart configures the server for handling requests
func (c *Config) PreStart(ctx context.Context, mux *http.ServeMux, server *http.Server) {
	c.oAuth = c.oAuthConf.NewOAuth(c.Server.Address, c.Server.Port)
}

// RegisterMuxes registers HTTP handlers with the webserver mux
func (c *Config) RegisterMuxes(mux *http.ServeMux) {
	mux.HandleFunc("/fireplace", fireplaceHandler)
	c.oAuth.RegisterMuxes(mux)
}

func fireplaceHandler(w http.ResponseWriter, r *http.Request) {
	switch r.Method {
	case http.MethodPost:
		state := fireplace.State{}
		if err := json.NewDecoder(r.Body).Decode(&state); err != nil {
			http.Error(w, fmt.Sprintf("Failed to unmarshal JSON: %v", err), http.StatusBadRequest)
			return
		}
		if err := state.Set(); err != nil {
			http.Error(w, fmt.Sprintf("Failed to set fireplace state: %v", err), http.StatusInternalServerError)
			return
		}
		w.WriteHeader(http.StatusCreated)
	default:
		http.Error(w, "Method Not Allowed.", http.StatusMethodNotAllowed)
	}
}
