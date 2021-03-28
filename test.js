const algosdk = require('algosdk');

const server = 'https://testnet-algorand.api.purestake.io/ps1';
const port = '';
const token = {
  'X-API-Key': 'iUYKksMBYO6odqKYA6PN65HzsvLJ8slV5zSugoGx'
}

//instantiate the algod wrapper
let algodclient = new algosdk.Algod(token, server, port);

var account1_mnemonic = "indoor project long invite vehicle toy travel image leopard true alpha mix know exhaust curious giggle day biology parent coffee pigeon black lunch abandon inquiry";
var account2_mnemonic = "shoulder grunt system render critic possible fortune float season weapon luxury jar patient build wheat siege behind patrol churn liberty catalog tongue drift above bring";
var account3_mnemonic = "indoor project long invite vehicle toy travel image leopard true alpha mix know exhaust curious giggle day biology parent coffee pigeon black lunch abandon inquiry";

var recoveredAccount1 = algosdk.mnemonicToSecretKey(account1_mnemonic);
var recoveredAccount2 = algosdk.mnemonicToSecretKey(account2_mnemonic);
var recoveredAccount3 = algosdk.mnemonicToSecretKey(account3_mnemonic);
console.log("Account One: " + recoveredAccount1.addr);
console.log("Account Two: " + recoveredAccount2.addr);
console.log("Account Three: " + recoveredAccount3.addr);

(async() => {
    var cp = {
      fee: 0, 
      firstRound: 0,  
      lastRound: 0, 
      genID: "",
      genHash: ""    
    }

    let params = await algodclient.getTransactionParams();
    cp["firstRound"] = params.lastRound;
    cp["lastRound"] = params.lastRound + parseInt(1000);
    
    let sFee = await algodclient.suggestedFee();
    cp["fee"] = 10; //sFee.fee;
    
    cp["genID"] = params.genesisID;
    cp["genHash"] = params.genesishashb64;
    console.log("cp", cp);
    
    let note = undefined;
    let addr = recoveredAccount1.addr;
    let defaultFrozen = false;
    let totalIssuance = 100;
    let unitName = "t-c"; 
    let assetName = "Tutorial-Coin";
    let assetURL = "http://someurl";
    let assetMetadataHash = "16efaa3924a6fd9d3a4824799a4ac65d";
    let manager = recoveredAccount2.addr;
    let reserve = recoveredAccount2.addr;
    let freeze = recoveredAccount2.addr;
    let clawback = recoveredAccount2.addr;
    
    console.log(addr, cp.fee, cp.firstRound, cp.lastRound, note, cp.genHash, cp.genID, totalIssuance, 0, defaultFrozen, manager, reserve, freeze, clawback, unitName, assetName, assetURL, assetMetadataHash);
    
    let txn = algosdk.makeAssetCreateTxn(addr, cp.fee, cp.firstRound, cp.lastRound, note, cp.genHash, cp.genID, totalIssuance, 0, defaultFrozen, manager, reserve, freeze, clawback, unitName, assetName, assetURL, assetMetadataHash);
    
    console.log(txn);
    
    let rawSignedTxn = txn.signTxn(recoveredAccount1.sk);
    console.log(rawSignedTxn);
    
    let tx = await algodclient.sendRawTransaction(rawSignedTxn);
    console.log("Transaction : " + tx.txId);
})()    
    