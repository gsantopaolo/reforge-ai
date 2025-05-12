
### 1. Stop JBoss EAP cleanly

```bash
/Users/gp/jboss/jboss-eap-8.0/bin/jboss-cli.sh --connect --command=":shutdown"
```

If you started JBoss with `standalone.sh`, you can also stop it by killing that process or hitting `Ctrl+C` in its terminal.

---

### 2. Clear out the deployments folder

```bash
cd /Users/gp/jboss/jboss-eap-8.0/standalone/deployments
rm -rf *
```

This removes all `.war`, marker files (`.dodeploy`, `.deployed`, etc.), and any other artifacts.

---

Connect to the CLI (while the server is running):

```bash
/Users/gp/jboss/jboss-eap-8.0/bin/jboss-cli.sh --connect
```

Undeploy the app:


```bash
undeploy kitchensink-1.0-SNAPSHOT.war

```
You should see a success message.

Exit the CLI:

```bash
quit
```

### 3. Build and Copy in your new WAR and trigger deployment

```bash
mvn clean package                                      
cp kitchensink/target/kitchensink-1.0-SNAPSHOT.war \
~/jboss/jboss-eap-8.0/standalone/deployments/kitchensink.war
touch ~/jboss/jboss-eap-8.0/standalone/deployments/kitchensink.war.dodeploy
```

Adjust the `cp` source path if your WAR is located elsewhere.

---

### 4. Start JBoss EAP again

```bash
/Users/gp/jboss/jboss-eap-8.0/bin/standalone.sh
```

Watch the server log for your new `kitchensink.war` to be deployed successfully.

```bash
tail -f ~/jboss/jboss-eap-8.0/standalone/log/server.log
```

### test the web service
```bash
curl http://localhost:8080/kitchensink/rest/members   
```