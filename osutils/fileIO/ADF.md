# Array Data File:
 Format was created to allow fast and disk space efficient way of storing 2 dimensional arrays onto disk.
`version 1.0 - 19.01.2018`

## 1. File Construction:  
### 1.1. Header
Header consists of 6 parts:
* 3 bytes - `ADF` as `0x41, 0x44, 0x46` code to check if file is actually in our format
* 1 byte - joint informations:
    * 4 bits representing format version
    * 4 bits representing data type (Consult part 1.3)
* 2 bytes - array width
* 2 bytes - array height
* 1 byte - end of header marker (`0xFF`)  
Header length: 9 bytes
### 1.2. Payload:
Simply series of values according to data type specification
### 1.3. Data formats:
* `0x0` - int16
* `0x1` - int32
