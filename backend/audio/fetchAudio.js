const exec = require('child_process').exec;

function call_python(id) {
    const cmd = 'python3 ' + process.cwd() + '/audio/fetchAudio.py ' + id;
    exec(cmd, (error, stdout, stderr) => {
        if (error) {
            console.log(stderr.toString())
            return;
        }
        console.log(stdout.toString());
    });
}

const fetchAudio = () => {
    call_python(Math.floor(Math.random() * 1000000));
};
  
exports.fetchAudio = fetchAudio;