/*---------------------------------------------------------------------------------------------
 *  Copyright (c) Microsoft Corporation. All rights reserved.
 *  Licensed under the MIT License. See License.txt in the project root for license information.
 *--------------------------------------------------------------------------------------------*/
if("--exec"===process.argv[2])process.argv.splice(1,2),require(process.argv[1]);else{const e=require("path");process.env.VSCODE_INJECT_NODE_MODULE_LOOKUP_PATH=process.env.VSCODE_INJECT_NODE_MODULE_LOOKUP_PATH||e.join(__dirname,"..","remote","node_modules"),require("./bootstrap").injectNodeModuleLookupPath(process.env.VSCODE_INJECT_NODE_MODULE_LOOKUP_PATH),require("./bootstrap-amd").load("vs/agent/remoteExtensionHostAgent")}
//# sourceMappingURL=https://ticino.blob.core.windows.net/sourcemaps/553cfb2c2205db5f15f3ee8395bbd5cf066d357d/core/remoteExtensionHostAgent.js.map
