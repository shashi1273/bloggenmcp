# Model Context Protocol (MCP) Architecture Overview

The Model Context Protocol (MCP) is built on a flexible, extensible architecture that enables seamless communication between LLM applications and integrations.

## Overview

MCP follows a client-server architecture where:

*   **Hosts** are LLM applications (like Claude Desktop or IDEs) that initiate connections
*   **Clients** maintain 1:1 connections with servers, inside the host application
*   **Servers** provide context, tools, and prompts to clients

## Core components

### Protocol layer

The protocol layer handles message framing, request/response linking, and high-level communication patterns.

Key classes include:

*   `Protocol`
*   `Client`
*   `Server`

### Transport layer

The transport layer handles the actual communication between clients and servers. MCP supports multiple transport mechanisms:

1.  **Stdio transport**
    *   Uses standard input/output for communication
    *   Ideal for local processes
2.  **Streamable HTTP transport**
    *   Uses HTTP with optional Server-Sent Events for streaming
    *   HTTP POST for client-to-server messages

All transports use [JSON-RPC](https://www.jsonrpc.org/specification) 2.0 to exchange messages. See the [specification](https://modelcontextprotocol.io/specification/2025-03-26/architecture) for detailed information about the Model Context Protocol message format.

### Message types

MCP has these main types of messages:

1.  **Requests** expect a response from the other side:

        interface Request {
          method: string;
          params?: { ... };
        }

2.  **Results** are successful responses to requests:

        interface Result {
          [key: string]: unknown;
        }

3.  **Errors** indicate that a request failed:

        interface Error {
          code: number;
          message: string;
          data?: unknown;
        }

4.  **Notifications** are one-way messages that don’t expect a response:

        interface Notification {
          method: string;
          params?: { ... };
        }

## Connection lifecycle

### 1. Initialization

ServerClientServerClient

