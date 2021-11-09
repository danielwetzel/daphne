/*
 * Copyright 2021 The DAPHNE Consortium
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

#ifndef SRC_PARSER_DAPHNEDSL_DAPHNEDSLVISITOR_H
#define SRC_PARSER_DAPHNEDSL_DAPHNEDSLVISITOR_H

#include <parser/daphnedsl/DaphneDSLBuiltins.h>
#include <parser/ParserUtils.h>
#include <parser/ScopedSymbolTable.h>

#include "antlr4-runtime.h"
#include "DaphneDSLGrammarParser.h"
#include "DaphneDSLGrammarVisitor.h"

#include <mlir/IR/Builders.h>
#include <mlir/IR/Value.h>

#include <string>
#include <unordered_map>

class DaphneDSLVisitor : public DaphneDSLGrammarVisitor {
    // By inheriting from DaphneDSLGrammarVisitor (as opposed to
    // DaphneDSLGrammarBaseVisitor), we ensure that any newly added visitor
    // function (e.g. after a change to the grammar file) needs to be
    // considered here. This is to force us not to forget anything.
    
    /**
     * The OpBuilder used to generate DaphneIR operations.
     */
    mlir::OpBuilder & builder;
    
    /**
     * Maps a variable name from the input DaphneDSL script to the MLIR SSA
     * value that has been assigned to it most recently.
     */
    ScopedSymbolTable symbolTable;
    
    /**
     * @brief General utilities for parsing to DaphneIR.
     */
    ParserUtils utils;
    
    /**
     * @brief Utility for creating DaphneIR operations for DaphneDSL built-in
     * functions.
     */
    DaphneDSLBuiltins builtins;
    
    std::unordered_map<std::string, std::string> args;
    
public:
    DaphneDSLVisitor(
            mlir::OpBuilder & builder,
            std::unordered_map<std::string, std::string> args
    ) : builder(builder), utils(builder), builtins(builder), args(args) {
        //
    };
    
    antlrcpp::Any visitScript(DaphneDSLGrammarParser::ScriptContext * ctx) override;

    antlrcpp::Any visitStatement(DaphneDSLGrammarParser::StatementContext * ctx) override;

    antlrcpp::Any visitBlockStatement(DaphneDSLGrammarParser::BlockStatementContext * ctx) override;

    antlrcpp::Any visitExprStatement(DaphneDSLGrammarParser::ExprStatementContext * ctx) override;

    antlrcpp::Any visitAssignStatement(DaphneDSLGrammarParser::AssignStatementContext * ctx) override;

    antlrcpp::Any visitIfStatement(DaphneDSLGrammarParser::IfStatementContext * ctx) override;

    antlrcpp::Any visitWhileStatement(DaphneDSLGrammarParser::WhileStatementContext * ctx) override;

    antlrcpp::Any visitForStatement(DaphneDSLGrammarParser::ForStatementContext * ctx) override;

    antlrcpp::Any visitLiteralExpr(DaphneDSLGrammarParser::LiteralExprContext * ctx) override;

    antlrcpp::Any visitArgExpr(DaphneDSLGrammarParser::ArgExprContext * ctx) override;

    antlrcpp::Any visitIdentifierExpr(DaphneDSLGrammarParser::IdentifierExprContext * ctx) override;

    antlrcpp::Any visitParanthesesExpr(DaphneDSLGrammarParser::ParanthesesExprContext * ctx) override;

    antlrcpp::Any visitCallExpr(DaphneDSLGrammarParser::CallExprContext * ctx) override;

    antlrcpp::Any visitCastExpr(DaphneDSLGrammarParser::CastExprContext * ctx) override;

    antlrcpp::Any visitRightIdxFilterExpr(DaphneDSLGrammarParser::RightIdxFilterExprContext * ctx) override;

    antlrcpp::Any visitRightIdxExtractExpr(DaphneDSLGrammarParser::RightIdxExtractExprContext * ctx) override;
    
    antlrcpp::Any visitMatmulExpr(DaphneDSLGrammarParser::MatmulExprContext * ctx) override;
    
    antlrcpp::Any visitPowExpr(DaphneDSLGrammarParser::PowExprContext * ctx) override;

    antlrcpp::Any visitModExpr(DaphneDSLGrammarParser::ModExprContext * ctx) override;
    
    antlrcpp::Any visitMulExpr(DaphneDSLGrammarParser::MulExprContext * ctx) override;
    
    antlrcpp::Any visitAddExpr(DaphneDSLGrammarParser::AddExprContext * ctx) override;
    
    antlrcpp::Any visitCmpExpr(DaphneDSLGrammarParser::CmpExprContext * ctx) override;
    
    antlrcpp::Any visitConjExpr(DaphneDSLGrammarParser::ConjExprContext * ctx) override;
    
    antlrcpp::Any visitDisjExpr(DaphneDSLGrammarParser::DisjExprContext * ctx) override;

    antlrcpp::Any visitLiteral(DaphneDSLGrammarParser::LiteralContext * ctx) override;

    antlrcpp::Any visitBoolLiteral(DaphneDSLGrammarParser::BoolLiteralContext * ctx) override;
};

#endif //SRC_PARSER_DAPHNEDSL_DAPHNEDSLVISITOR_H