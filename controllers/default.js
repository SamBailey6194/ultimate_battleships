const Pty = require('node-pty');
const fs = require('fs');
const path = require('path');

exports.install = function () {

    ROUTE('/');
    WEBSOCKET('/', socket, ['raw']);

    // Handle SIGTERM (graceful shutdown)
    process.on('SIGTERM', () => {
        console.log('Received SIGTERM, cleaning up...');
        if (client.tty) {
            client.tty.kill(9);
            console.log('Terminal process killed');
        }
        process.exit(0);
    })
};

function socket() {

    this.encodedecode = false;
    this.autodestroy();

    this.on('open', function (client) {

        const scriptPath = path.join(__dirname, '..', 'python_scripts', 'main.py');
        // Spawn terminal
        client.tty = Pty.spawn('python3', [scriptPath], {
            name: 'xterm-color',
            cols: 80,
            rows: 24,
            cwd: __dirname,
            env: process.env
        });

        client.tty.on('exit', function (code, signal) {
            client.tty = null;
            client.close();
            console.log("Process killed");
        });

        client.tty.on('data', function (data) {
            client.send(data);
        });

    });

    this.on('close', function (client) {
        if (client.tty) {
            client.tty.kill(9);
            client.tty = null;
            console.log("Process killed and terminal unloaded");
        }
    });

    this.on('message', function (client, msg) {
        client.tty && client.tty.write(msg);
    });
}

// const credsPath = path.join(__dirname, '..', 'creds.json');
// if (process.env.CREDS != null) {
//     console.log("Creating creds.json file.");
//     fs.writeFile(credsPath, process.env.CREDS, 'utf8', function (err) {
//         if (err) {
//             console.log('Error writing file: ', err);
//             socket.emit("console_output", "Error saving credentials: " + err);
//         } else {
//             console.log('creds.json written successfully');
//             fs.access(credsPath, fs.constants.F_OK, (err) => {
//                 if (err) console.log('File NOT found after writing:', err);
//                 else console.log('Confirmed creds.json exists at:', credsPath)
//             })
//         }
//     });
// }