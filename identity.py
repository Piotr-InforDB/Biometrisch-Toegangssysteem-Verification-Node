import uuid
import platform
import subprocess
import json

class Identity:
    def __init__(self):
        self.name = "Verification Node"
        self.type = "verification"
        self.id = self.get_unique_id()

    def get_identity_json(self):
        data = {
            "name": self.name,
            "type": self.type,
            "id": self.id
        }
        return json.dumps(data)

    def get_unique_id(self):
        system = platform.system()

        try:
            mac = ''.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff)
                            for elements in range(0, 2 * 6, 2)][::-1])
            return mac.upper()
        except:
            if system == 'Linux':
                try:
                    with open('/proc/cpuinfo', 'r') as f:
                        for line in f:
                            if line.startswith('Serial'):
                                return line.split(':')[1].strip()
                except:
                    pass

            elif system == 'Windows':
                try:
                    output = subprocess.check_output('wmic csproduct get uuid').decode()
                    return output.split('\n')[1].strip()
                except:
                    pass

            try:
                with open('.machine_id', 'r') as f:
                    return f.read().strip()
            except FileNotFoundError:
                machine_id = str(uuid.uuid4())
                with open('.machine_id', 'w') as f:
                    f.write(machine_id)
                return machine_id