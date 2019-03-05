pragma solidity ^0.5.0;

interface tokenRecipient {
  function receiveApproval(address _from, uint256 _value, address _token, bytes calldata _extraData) external;
}

contract TexasBlockchainToken {
  string public name;
  string public symbol;
  uint8 public decimals = 1;
  uint256 private _totalSupply;
  address private _creator;

  mapping (address => uint256) private balances;
  mapping (address => mapping (address => uint256)) private allowance;

  event Transfer(address indexed from, address indexed to, uint256 value);
  event Approval(address indexed _owner, address indexed _spender, uint256 _value);
  event Burn(address indexed from, uint256 value);

  constructor(uint256 initialSupply, string memory tokenName, string memory tokenSymbol) public {
    balances[msg.sender] = initialSupply;
    name = tokenName;
    symbol = tokenSymbol;
    _totalSupply = initialSupply;
    _creator = msg.sender;
  }

  function totalSupply() public view returns (uint256) {
    return _totalSupply;
  }

  function _transfer(address _from, address _to, uint _value) internal {
    require(_to != address(0x0));
    require(balances[_from] >= _value);
    require(balances[_to] + _value >= balances[_to]);

    uint previousBalances = balances[_from] + balances[_to];
    balances[_from] -= _value;
    balances[_to] += _value;

    emit Transfer(msg.sender, _to, _value);

    assert(balances[_from] + balances[_to] == previousBalances);
  }

  function transfer(address _to, uint256 _value) public returns (bool success) {
    _transfer(msg.sender, _to, _value);
    return true;
  }

  function balanceOf(address _owner) public view returns (uint256 balance) {
    return balances[_owner];
  }

  function transferFrom(address _from, address _to, uint256 _value) public returns (bool success) {
    require(_value <= allowance[_from][msg.sender]);
    allowance[_from][msg.sender] -= _value;
    _transfer(_from, _to, _value);
    return true;
  }

  function approve(address _spender, uint256 _value) public returns (bool success) {
    allowance[msg.sender][_spender] = _value;
    emit Approval(msg.sender, _spender, _value);
    return true;
  }

  function approveAndCall(address _spender, uint256 _value, bytes memory _extraData) public returns (bool success) {
    tokenRecipient spender = tokenRecipient(_spender);
    if (approve(_spender, _value)) {
      spender.receiveApproval(msg.sender, _value, address(this), _extraData);
      return true;
    }
  }

  function burn(uint256 _value) public returns (bool success) {
    require(balances[msg.sender] >= _value);
    balances[msg.sender] -= _value;
    _totalSupply -= _value;
    emit Burn(msg.sender, _value);
    return true;
  }

  function burnFrom(address _from, uint256 _value) public returns (bool success) {
    require(balances[_from] >= _value);
    require(_value <= allowance[_from][msg.sender]);
    balances[_from] -= _value;
    allowance[_from][msg.sender] -= _value;
    _totalSupply -= _value;
    emit Burn(_from, _value);
    return true;
  }

  function mint(uint256 _amount) public returns (bool success) {
    require(msg.sender == _creator);
    require(balances[_creator] + _amount > balances[_creator]);
    balances[_creator] += _amount;
    return true;
  }

  function destroy() public returns (bool success) {
    require(msg.sender == _creator);
    selfdestruct(msg.sender);
    return true;
  }
}
