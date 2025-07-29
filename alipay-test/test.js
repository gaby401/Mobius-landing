const AlipaySdk = require('alipay-sdk').default;
const fs = require('fs');

// PRIVATE KEY from .env (ali_private_key multiline-friendly)
const privateKey = `
-----BEGIN RSA PRIVATE KEY-----
MIIEpQIBAAKCAQEAs7XCQsubiQtpHgZRmucIWjj49KBfOH+APm/L5QrNRnand137
camPj9i61k3fCScA9MzGCDgBNYAoQrPxwEfCykXtfa6hlgHrHOMMrEC2vAP7OaNR
RmzLRQTX+yhMUpt/RQcV18F9xskAR39z51DQbRW7U3959sKQbAG+aGZDpYHHFs56
c0R+0dkGYncbP872Ec1pv27XmWzobX1nirX2QWvlvsa+7DEnAsPTzSQZm0Mpx/uy
LG/Ub4UySu7fGhty5qaiNHHPqBPp3BLRiqYBOW7ZMgwqIG2ZRzbGOEVx4axfSc2i
ldhsqQy69ZkOGavc0w9M9FnHsvUZu4f33xtypwIDAQABAoIBAQCNtP9v6FnHIQZM
tLLYsOE3M8GsNGGhjXi0wzdGbtQbgijfyW4i3I/l4ALERjdfYjAw2OA3TuI1K8+T
eY1iD7QcCDQTbQbh4LVi2+78TTNK4uDRPGU0YUmQLReaZtZ4NUGQTtv8fAkQHSNp
PalJd8JComZKmzSzTgzP/jgE3s7szCyCIz96a+yd9w+1/sJ+RzL7+PaRP51boyOl
vq4B8IIJKagmXb5VSweUNtoYh/crGkRBNAcX9ttrn45c4DV2KjC9J0PXF2Cbdg0P
CUR8LB8A+HIcYzgda7R4DOPU8uulMuavJd/wzsUBzGy+S+1dnH0N54sKM1zqScjS
6UpAIfVxAoGBAN9xxDc8vCAMbKcv7gMLk4+5457K2alCUaBjJWaVeaFem+yxZMT6
GvZ9rsjQRnxttPQ0CCb8bAj2E4MYqlKWDHnSsiTTKiXhgzhqBNz7gY+kl5WbLnUk
l+B9jAXkDj61AuvZXjZ+si0gm0dIU5akpVSNKFX0WCDv01wDoAvsv65LAoGBAM3k
vx20cLIu2cWqXU0LpwTMWLRiky/FSRPSz4JgaZleR/7q2whdp9XetA6ML/TsZYrL
hWkQ72sK0mvaWILGYYwrAoEDqGvekV1Bjj/83W5G3JQ47SkB4RspG/HyUNt+EbVL
TJUBSjkmVPwjpJSRUnNB3eytfB9ZI0qCrqkS7GOVAoGBAI42CysY1acUIUcbI0H+
6TDNn8hd1MB8PBV3ZMNwmRQScezoTnlrsSN2hHq8zE+/Ry8xuoqNl3jwnSSP2z9q
zo/ugIEdgLLRX8HVADlhPWmd2PhX5u6ZlqxDW44YQtS4Qh63ntXSNzavjQSGTOUQ
70Tr/mMOe9SirwPeLsvIJ4sXAoGAEa/68xRTMhtwPdja1wmPOYxMeoKVXl82XeuY
Q/0AVVqSGMYYNunEx0ywbyd/3yyHtJqzRUldJ/bwCK/jNqjQLHhtaKPlzg56smY1
UC3q39RakqkpRoKQ0gKAEhLc+14jK03isFJCDBLM7jQpqVGqoZgg9noY1aCUtYvw
cTnc8NkCgYEAyoGNgpbekD+rxHHnb6erpFSYO1v6DKmBqDtNpO98vnZ7frTQo3IT
/Njv/Pt/tI/tvTWM5PGpGaHuLcIp7F2lqFFxKepiNbQmHeCLtWOEC11S7yGaS7pJ
UEAOyuhUrPd0xFZr/wypGJ+7daNr+WExBSQJ6kaj+iAb0Aua/ejylb8=
-----END RSA PRIVATE KEY-----
`;

const alipaySdk = new AlipaySdk({
  appId: '2018042560075209',
  privateKey: privateKey,
  alipayPublicKey: '', // optional, for verification
  gateway: 'https://openapi.alipay.com/gateway.do',
  timeout: 5000,
  camelcase: true
});

// Make a test API call (OAuth grant is easiest to test)
(async () => {
  try {
    const result = await alipaySdk.exec('alipay.system.oauth.token', {
      grantType: 'authorization_code',
      code: 'TEST_CODE_SHOULD_FAIL'
    });
    console.log('📦 Alipay Response:', result);
  } catch (e) {
    console.error('❌ Alipay API Error:', e.message || e);
  }
})();
