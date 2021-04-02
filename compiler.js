
var variables = ['abc', 'yeet'];

var tt_assign = 'assign'; //imma implement these next
var tt_equal = 'equals';
var tt_greatEQ = 'greatEQ';
var tt_lessEQ = 'lessEQ';
var tt_less = 'less';
var tt_great = 'greater';

var tt_int = 'int';
var tt_float = 'float'; //doesnt support on urcl yet
var tt_plus = 'plus';
var tt_minus = 'minus';
var tt_mult = 'mult';
var tt_div = 'div';
var tt_exp = 'exp';
var tt_sqrt = 'sqrt';
var tt_lparen = 'lparen';
var tt_rparen = 'rparen';

//LEXER

function lexer() {
    var input = document.getElementById('input').value;

    var tokens = [];
    var errors = "Lexing errors:";

    let lastToken = '';
    let leftP = false;

    var lines = input.split("\n");
    for(let i = 0; i < lines.length; i++) {
        for(let j = 0; j < lines[i].length; j++) {
            while(lines[i][j] === " " || lines[i][j] === "\t" || lines[i][j] === "\n") {
                j++;
            }

            if(lines[i][j] === '+') {
                tokens.push(tt_plus);
                lastToken = tt_plus;
            }
            else if(lines[i][j] === '-') {
                tokens.push(tt_minus);
                lastToken = tt_minus;
            }
            else if((lines[i][j] === '*') && (lines[i][j+1] !== '*')) {
                if((((lastToken === tt_div) || (lastToken === tt_sqrt) || (lastToken === tt_mult))) || ((lastToken === tt_lparen) || (lastToken === tt_minus)) || (lastToken === tt_plus)) {        
                    errors += '\n' + 'Invalid combination of operators at position ' + j + ' at line ' + i;
                }
                tokens.push(tt_mult);
                lastToken = tt_mult;
            }
            else if(lines[i][j] === '/') {
                if((((lastToken === tt_div) || (lastToken === tt_exp)) || ((lastToken === tt_sqrt) || (lastToken === tt_mult))) || ((lastToken === tt_lparen) || (lastToken === tt_minus)) || (lastToken === tt_plus)) {        
                    errors += '\n' + 'Invalid combination of operators at position ' + j + ' at line ' + i;
                }
                tokens.push(tt_div);
                lastToken = tt_div;
            }
            else if((lines[i][j] === '*') && (lines[i][j+1] === '*')) {
                if((((lastToken === tt_div) || (lastToken === tt_exp)) || (lastToken === tt_mult)) || ((lastToken === tt_lparen) || (lastToken === tt_minus)) || (lastToken === tt_plus)) {        
                    errors += '\n' + 'Invalid combination of operators at position ' + j + ' at line ' + i;
                }
                tokens.push(tt_exp);
                lastToken = tt_exp;
                j++;
            }
            else if(lines[i][j] === '(') {
                if(((lastToken === tt_int) || (lastToken === tt_float)) || ((lastToken === tt_rparen) || (lastToken === 'var'))) {
                    tokens.push(tt_mult);
                }
                leftP = true;
                tokens.push(tt_lparen);
                lastToken = tt_lparen;
            }
            else if(lines[i][j] === ')') {
                if(!leftP) {
                    errors += '\n' + 'missing parenthesis before position ' + j + ' at line ' + i;
                }
                if(lastToken === tt_lparen) {
                    errors += '\n' + 'Empty parenthesis at position ' + j + ' at line ' + i;
                }
                else if((((lastToken === tt_div) || (lastToken === tt_exp)) || ((lastToken === tt_sqrt) || (lastToken === tt_mult))) || ((lastToken === tt_lparen) || (lastToken === tt_minus)) || (lastToken === tt_plus)) {        
                    errors += '\n' + 'Invalid combination of operators at position ' + j + ' at line ' + i;
                }
                
                tokens.push(tt_rparen);
                lastToken = tt_rparen;
            }
            else if(/^[0-9.]$/.test(lines[i][j])) {
                let temp = (makeNumber(i, j, lines));
                if(lastToken === tt_rparen) {
                    tokens.push(tt_mult);
                }
                tokens.push(`${temp[0][0]}:${temp[0][1]}`);
                j = temp[1];
                j--;
                lastToken = temp[0][0];
            }
            else if(/^[a-zA-Z]$/.test(lines[i][j])) {
                let temp = makeVar(i, j, lines);
                let bool = false;
                if(lastToken === tt_rparen) {
                    tokens.push(tt_mult);
                }
                for(let k = 0; k < variables.length; k++) {
                    if(temp[0] === variables[k]) {
                        tokens.push('var:' + temp[0]);
                        bool = true;
                        lastToken = 'var';
                        break
                    }
                }
                j = temp[1];
                j--;
                if(bool === false) {
                    errors += '\n' + 'Unknown variable "' + temp[0] + '" at position ' + j + ' at line ' + i;
                }
            }
            else {
                if(lines[i][j] === undefined) {
                    errors += '\n' + 'Please fill the field with program first';
                }
                else {
                    errors += '\n' + 'illegal char "' + lines[i][j] + '" at position ' + j + ' at line ' + i;
                }
            }
        }
        console.log(tokens);
        console.log(errors);
        if(errors === 'Lexing errors:') {
            errors = '';
        }
        document.getElementById('lexerOutput').innerHTML = tokens + '\n' + errors;
        return tokens
    }
    
    
}


//called by lexer
function makeNumber(i, j, lines) {
    let numStr = '';
    let dots = 0;
    let E = 0;
    let tt;
    while(/^[0-9.e]$/.test(lines[i][j])) { 
        if((lines[i][j] === '.') && (dots < 1)) {
            dots++;
            numStr += '.';
        }
        else if((lines[i][j] === '.') && (dots >= 1)) {
            errors += '\n' + 'extra point used  at position ' + j + ' at line ' + i + ' in operand ' + numStr;
        }
        else if((lines[i][j] === 'e') && (E < 1)) {
            let exponent = '';
            E++;
            while(/^[0-9.e]$/.test(lines[i][j])) {
                j++;
                exponent += lines[i][j];
            }
            numStr = parseFloat(numStr);
            numStr = numStr * (Math.pow(10, parseInt(exponent)));
            numStr = numStr.toString(10);
            numStr = numStr.substring(0, 7);
            if((parseFloat(numStr) % 1) === 0) {
                dots = 0;
            }
        }
        else if((lines[i][j] === 'e') && (E >= 1)) {
            errors += '\n' + 'extra "e" used  at position ' + j + ' at line ' + i + ' in operand ' + numStr;
        }
        else {
            numStr += lines[i][j];
        }
        j++;
    }
    let out = [[], j];
    if(dots === 0) {
        tt = 'int';
        out[0].push(tt);
        out[0].push(parseInt(numStr, 10));
    }
    else {
        tt = 'float';
        out[0].push(tt);
        out[0].push(parseFloat(numStr, 10));
    }
    return out
}

//called by lexer
function makeVar(i, j, lines) {
    let varStr = '';
    while(/^[0-9a-zA-Z_]$/.test(lines[i][j])) {
        varStr += lines[i][j];
        j++;
    }
    let out = [varStr, j];
    return out
}

//PARSER

function parser() {
    var input = lexer();

    var stack = [];
    var queue = [];
    var errors = 'Parsing errors:';
    for(let i = 0; i < input.length; i++) {
        if(input[i].startsWith(tt_int) || input[i].startsWith(tt_float) || input[i].startsWith('var')) {
            queue.push(input[i]);
        }
        else if(input[i].startsWith(tt_exp)) {
            stack.push(input[i]);
        }
        else if(input[i] === tt_lparen) {
            stack.push(input[i]);
        }
        else if((input[i] === tt_minus) || ((input[i]) === tt_plus)) {
            while((stack[stack.length-1] === tt_div) || (stack[stack.length-1] === tt_mult) || (stack[stack.length-1] === tt_plus) || (stack[stack.length-1] === tt_minus)) {
                queue.push(stack.pop());
            }
            stack.push(input[i]);
        }
        else if((input[i] === tt_div) || (input[i] === tt_mult)) {
            while((stack[stack.length-1] === tt_div) || (stack[stack.length-1] === tt_mult)) {
                queue.push(stack.pop());
            }
            stack.push(input[i]);
        }
        else if(input[i] === tt_rparen) {
            while(stack[stack.length-1] !== tt_lparen) {
                queue.push(stack.pop());
            }
            stack.pop();
        }
        else {
            console.log('something went very wrong :/');
            errors += '\n' + 'unknown type of lexed output, pls fix this error on the lexer'
        }
   }
   let temp = stack.length;
    for(let i = 0; i < temp; i++) {
        queue.push(stack.pop());
    }
    if(errors === 'Parsing errors:') {
        errors = '';
    }
    document.getElementById('parserOutput').innerHTML = queue + '\n' + errors;
    return queue
}

//interpreter           gotta fix outputs calculated before any variable beeing shown before the instruction

function interpreter() {
    var input = parser();
    var useLibMath = false;
    var useVar = false;
    var stack = [];
    var output = '';
    let firstOp;
    let secondOp;
    var outReg = `R${variables.length + 1}`;
    var inReg = `R${variables.length + 2}`;
    var errors = 'interpreting errors:';
    for(let i = 0; i < input.length; i++) {
        if(input[i].startsWith('var')) {
            input[i] = replaceVar(input[i]);
            useVar = true;
            stack.push(input[i]);
        }
        else if(input[i].startsWith(tt_int) || input[i].startsWith(tt_float)) {
            stack.push(input[i]);
        }
        else if(input[i] === tt_plus) {
            secondOp = stack.pop();
            firstOp = stack.pop();
            if((firstOp.startsWith(tt_int) || firstOp.startsWith(tt_float)) && secondOp.startsWith(tt_int) || secondOp.startsWith(tt_float)) {
                output = operation(tt_plus, firstOp, secondOp);
                stack.push(output);
            }
            else {
                output += 'MOV ' + inReg + ', ' + outReg + '\n';
                output += 'ADD ' + outReg + ', ' + firstOp + ', ' + secondOp + '\n';
                stack.push(outReg);
            }
        }
        else if(input[i] === tt_minus) {
            secondOp = stack.pop();
            firstOp = stack.pop();
            if((firstOp.startsWith(tt_int) || firstOp.startsWith(tt_float)) && secondOp.startsWith(tt_int) || secondOp.startsWith(tt_float)) {
                output = operation(tt_minus, firstOp, secondOp);
                stack.push(output);
            }
            else {
                output += 'MOV ' + inReg + ', ' + outReg + '\n';
                output += 'SUB ' + outReg + ', ' + firstOp + ', ' + secondOp + '\n';
                stack.push(outReg);
            }
        }
        else if(input[i] === tt_div) {
            secondOp = stack.pop();
            firstOp = stack.pop();
            if((firstOp.startsWith(tt_int) || firstOp.startsWith(tt_float)) && secondOp.startsWith(tt_int) || secondOp.startsWith(tt_float)) {
                output = operation(tt_div, firstOp, secondOp);
                stack.push(output);
            }
            else {
                output += 'MOV ' + inReg + ', ' + outReg + '\n';
                output += 'DIV ' + outReg + ', ' + firstOp + ', ' + secondOp + '\n';
                stack.push(outReg);
            }
        }
        else if(input[i] === tt_mult) {
            secondOp = stack.pop();
            firstOp = stack.pop();
            if((firstOp.startsWith(tt_int) || firstOp.startsWith(tt_float)) && secondOp.startsWith(tt_int) || secondOp.startsWith(tt_float)) {
                output = operation(tt_mult, firstOp, secondOp);
                stack.push(output);
            }
            else {
                output += 'MOV ' + inReg + ', ' + outReg + '\n';
                output += 'MLT ' + outReg + ', ' + firstOp + ', ' + secondOp + '\n';
                stack.push(outReg);
            }
        }
        else if(input[i] === tt_exp) {
            secondOp = stack.pop();
            firstOp = stack.pop();
            if((firstOp.startsWith(tt_int) || firstOp.startsWith(tt_float)) && secondOp.startsWith(tt_int) || secondOp.startsWith(tt_float)) {
                output = operation(tt_exp, firstOp, secondOp);
                stack.push(output);
            }
            else {
                useLibMath = true;
                output += 'MOV ' + inReg + ', ' + outReg + '\n';
                output += 'CAL .advmath_EXP(' + outReg + ',' + firstOp + ',' + secondOp + ')\n';
                stack.push(outReg);
            }
        }
    }

    if(errors === 'interpreting errors:') {
        errors = '';
    }

    output = replaceInt(output);

    //optimizing the output code

    if(output.startsWith(`MOV R${variables.length + 2}, R${variables.length + 1}\n`)) {
        output = output.substring(11);
    }
    console.log(output);
    /*for(let i = 0; i < output.length; i++) {
        while(/^[0-9]$/.test(output[i])) {

            break
        }    
    }*/

    if(output.includes('float:')) {
        output = `IMPORT float\n${output}`;
    }

    if(useLibMath) {
        output = `IMPORT advmath\n${output}`;
    }


    document.getElementById('output').innerHTML = output + '\n' + errors;
    return output
}

//called by interpreter
function replaceVar(input) {
    let output;
    input = input.substring(4);
    output = `R${(variables.indexOf(input) + 1)}`;
    return output
}

//called by interpreter
function replaceInt(input) {
    let output = '';
    for(let i = 0; i < input.length; i++) {
        if((input[i] === 'i') && (input[i+1] === 'n') && (input[i+2] === 't') && (input[i+3] === ':')) {
            i += 4;
        }
        output += input[i];
    }
    return output
}

//called by interpreter
function operation(operator, numA, numB) {
    let output;
    let isFloat = false;
    if(numA.startsWith(tt_int)) {
        numA = numA.substring(4);
        numA = parseInt(numA, 10);
    }
    else {
        isFloat = true;
        numA = numA.substring(6);
        numA = parseFloat(numA);
    }
    if(numB.startsWith(tt_int)) {
        numB = numB.substring(4);
        numB = parseInt(numB, 10);
    }
    else {
        isFloat = true;
        numB = numB.substring(6);
        numB = parseFloat(numB);
    }
    switch (operator) {
        case tt_plus:
            output = numA + numB;
            break;
        case tt_minus:
            output = numA - numB;
            break;
        case tt_mult:
            output = numA * numB;
            break;
        case tt_div:
            output = numA / numB;
            Math.floor(output);
            break;
        case tt_exp:
            output = Math.pow(numA, numB);
    }
    if(isFloat) {
        output = `${tt_float}:${output.toString()}`;
    }
    else {
        output = `${tt_int}:${output.toString()}`;
    }
    return output
}

