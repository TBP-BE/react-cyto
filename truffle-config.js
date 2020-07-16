const path = require("path");

module.exports = {
  // See <http://truffleframework.com/docs/advanced/configuration>
  // to customize your Truffle configuration!
  contracts_build_directory: path.join(__dirname, "client/src/contracts"),
  networks: {
    ganache: {
      host: "127.0.0.1",
      port: 8545,
      network_id: "*"
    },

    development: {
	    host:"127.0.0.1",
      port: 8545,
      network_id:"*"
	
    }
  }
};

/*const path = require("path");
const HDWalletProvider = require("./wallet-provider.js");
module.exports = {
  contracts_build_directory: path.join(__dirname, "client/src/contracts"),
    networks: {
        testrpc: {
            provider: () => {
                const testrpcMnemonic = "dumb popular muscle wild poverty order budget pride mask sample balcony witness";
                return new HDWalletProvider(testrpcMnemonic, "http://localhost:8545", 0, 10);
            },
            network_id: "*",
            gas: 4700000
        }
}
};*/