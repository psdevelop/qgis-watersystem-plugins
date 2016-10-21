# -*- coding: utf-8 -*-
__author__ = 'POLTAROKOV SP'


from PyQt4 import QtCore, QtGui, QtSql, Qt

class materialRelSqlModel(QtSql.QSqlRelationalTableModel):
    def __init__(self, QObject_parent=None):
        super(materialRelSqlModel, self).__init__(QObject_parent)

    #def flags(self, QModelIndex):
        #Qt::ItemFlags flags = QSqlQueryModel::flags(index);
        #if (index.column() == 1 || index.column() == 2)
        #    flags |= Qt::ItemIsEditable;
        #return flags;
        #super(materialRelSqlModel, self).flags(QModelIndex)

    #def __init__(self, parent=None):
    #   QtSql.QSqlQueryModel.__init__(self,parent)

    def toint(self, value):
        try:
            return int(value)
        except Exception:
            return 0

    def setData(self, QModelIndex, p_object, int_role=None):
        #if (index.column() < 1 || index.column() > 2)
            #return false;

        primaryKeyIndex = QtSql.QSqlRelationalTableModel.index(self,QModelIndex.row(), 0)
        id = QtSql.QSqlRelationalTableModel.data(self,primaryKeyIndex)

        #clear();

        #bool ok;

        if (QModelIndex.column() == 4):
            ok = self.setStrData("diametr", id, p_object);
        if (QModelIndex.column() == 7):
            ok = self.setStrData("injdeep", id, p_object);#
        if (QModelIndex.column() == 1):
            ok = self.setStrData("description", id, p_object);
        if (QModelIndex.column() == 2) and (self.toint(p_object)>0):
            ok = self.setStrData("material", id, p_object);
        #} else {
        #ok = setStrData(id, value.toString());}
        #refresh();
        #return ok;
        #print "[[["
        #print str(QModelIndex.column())
        #print "==="
        #print str(id)
        #print "==="
        #print p_object
        #print "]]]"

        return super(materialRelSqlModel, self).setData(QModelIndex, p_object, int_role)

    #def refresh(self):
        #self.setQuery("SELECT * FROM...")
        #self.setHeaderData(0, QtCore.Qt.Horizontal, "ID")

    def setStrData(self, field_name, objId, strData):
        setQ = QtSql.QSqlQuery()
        setQ.prepare("update injoutpipes set "+field_name+" = :val where id = :id")
        setQ.bindValue(":val", strData)
        setQ.bindValue(":id", objId)
        return setQ.exec_()

    #def data(self, QModelIndex, int_role=None):
        #QVariant value = QSqlQueryModel::data(index, role);
        #if (value.isValid() && role == Qt::DisplayRole) {
        #if (index.column() == 0)
        #return value.toString().prepend("#");
        #else if (index.column() == 2)
            #return value.toString().toUpper();}
        #if (role == Qt::TextColorRole && index.column() == 1)
            #return QVariant::fromValue(QColor(Qt::blue));
        #return value;
        #return super(myCustomSqlModel, self).data(QModelIndex, int_role)

#include <QtWidgets>
#include <QtSql>

#include "../connection.h"

# void initializeModel(QSqlRelationalTableModel *model)
# {
#     model->setTable("employee");
#
#     model->setEditStrategy(QSqlTableModel::OnManualSubmit);
#     model->setRelation(2, QSqlRelation("city", "id", "name"));
#     model->setRelation(3, QSqlRelation("country", "id", "name"));
#
#     model->setHeaderData(0, Qt::Horizontal, QObject::tr("ID"));
#     model->setHeaderData(1, Qt::Horizontal, QObject::tr("Name"));
#     model->setHeaderData(2, Qt::Horizontal, QObject::tr("City"));
#     model->setHeaderData(3, Qt::Horizontal, QObject::tr("Country"));
#
#     model->select();
# }
#
# QTableView *createView(const QString &title, QSqlTableModel *model)
# {
#     QTableView *view = new QTableView;
#     view->setModel(model);
#     view->setItemDelegate(new QSqlRelationalDelegate(view));
#     view->setWindowTitle(title);
#     return view;
# }
#
# void createRelationalTables()
# {
#     QSqlQuery query;
#     query.exec("create table employee(id int primary key, name varchar(20), city int, country int)");
#     query.exec("insert into employee values(1, 'Espen', 5000, 47)");
#     query.exec("insert into employee values(2, 'Harald', 80000, 49)");
#     query.exec("insert into employee values(3, 'Sam', 100, 1)");
#
#     query.exec("create table city(id int, name varchar(20))");
#     query.exec("insert into city values(100, 'San Jose')");
#     query.exec("insert into city values(5000, 'Oslo')");
#     query.exec("insert into city values(80000, 'Munich')");
#
#     query.exec("create table country(id int, name varchar(20))");
#     query.exec("insert into country values(1, 'USA')");
#     query.exec("insert into country values(47, 'Norway')");
#     query.exec("insert into country values(49, 'Germany')");
# }
#
# int main(int argc, char *argv[])
# {
#     QApplication app(argc, argv);
#     if (!createConnection())
#         return 1;
#     createRelationalTables();
#
#     QSqlRelationalTableModel model;
#
#     initializeModel(&model);
#
#     QTableView *view = createView(QObject::tr("Relational Table Model"), &model);
#     view->show();
#
#     return app.exec();
# }


