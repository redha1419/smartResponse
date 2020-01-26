const axios = require('axios');

const getAccessToken = () => {
    //request auth
    /*
    return axios.get('https://auth.aa.cityiq.io/oauth/token?grant_type=client_credentials', {
        params: {
            grant_type: 'client_credentials'
        },
        auth: {
            //HARDCODED FOR NOW
            username: 'Hackathon.CITM.Hamilton',
            password: 'Wm,yb&G`KB\2}d<s'
        },
        headers: {
            'Authorization': 'Basic aWMuc3RhZ2Uuc2ltLmRldmVsb3A6ZGV2'
        }
    });
    */

    return process.env.API_TOKEN;
};

exports.getAccessToken = getAccessToken;